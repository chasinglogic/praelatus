from guardian.shortcuts import get_objects_for_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.db.models import Q
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from fields.models import Field, FieldValue
from labels.models import Label
from projects.models import Project
from rest_framework import generics
from workflows.models import Transition
from workflows.tasks import fire_hooks

from .forms import AttachmentForm
from .models import Comment, FieldScheme, Ticket, TicketType, Attachment
from .serializers import (CommentSerializer, TicketSerializer,
                          TicketTypeSerializer)

# API


class TicketList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        projects = get_objects_for_user(self.request.user, 'projects.view_project')
        return Ticket.objects.filter(project__key__in=[p.key for p in projects]).all()


class TicketDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    lookup_field = 'key'


class TicketTypeList(generics.ListCreateAPIView):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class TicketTypeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer


class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'key'

    def get_queryset(self):
        return Comment.objects.\
            filter(ticket__key=self.kwargs.get(self.lookup_url_kwarg)).\
            all()

# UI


def show(request, key=''):
    """Show a single Ticket."""
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('ticket_type').\
        prefetch_related('status').\
        prefetch_related('labels').\
        prefetch_related('fields').\
        prefetch_related('comments').\
        all()

    if len(t) == 0:
        raise Http404('No ticket with that key found.')

    attachment_form = AttachmentForm()
    return render(request, 'tickets/show.html', {'ticket': t[0], 'attachment_form': attachment_form})


@login_required
def create(request, project_key='', ticket_type=''):
    proj = Project.objects.get(key=project_key)
    if not request.user.has_perm('projects.create_content', proj):
        raise PermissionDenied

    if request.method == 'POST':
        ttype = TicketType.objects.get(name=ticket_type)

        workflows = proj.workflow_schemes.filter(ticket_type=ttype).all()
        if len(workflows) == 0:
            # Get the default workflow
            workflow = proj.workflow_schemes.\
                filter(ticket_type=None).all()[0].workflow
        else:
            workflow = workflows[0].workflow

        t = Ticket(
            key=project_key + '-' + str(proj.content.count() + 1),
            summary=request.POST['summary'],
            project=proj,
            reporter=request.user,
            ticket_type=ttype,
            status=workflow.create_status,
            workflow=workflow,
            description=request.POST['description']
        )

        t.save()

        fields = [f for f in request.POST.keys()
                  if f not in ['labels', 'summary', 'description',
                               'csrfmiddlewaretoken']]

        for f in fields:
            field = Field.objects.get(name=f)
            value = FieldValue(field=field, content_object=t)
            value.set_value(request.POST[f])
            value.save()

        return redirect('/tickets/' + t.key)

    fs = FieldScheme.objects.\
        filter(project=proj,
               ticket_type__name=ticket_type).\
        all()

    if len(fs) == 0:
        fs = FieldScheme.objects.\
            filter(project=proj,
                   ticket_type=None).\
            all()

    return render(request, 'tickets/create.html', {'fs': fs[0]})


def create_prompt(request):
    projects = get_objects_for_user(request.user, 'projects.create_content')
    ticket_types = TicketType.objects.all()
    return render(request, 'tickets/create_prompt.html', {
        'projects': projects,
        'ticket_types': ticket_types
    })


@login_required
def dashboard(request):
    return render(request, 'dashboard/index.html')


@login_required
def transition(request, key=''):
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('status').\
        all()
    if len(t) == 0:
        raise Http404('No ticket with that key found.')

    tk = t[0]
    tr = Transition.objects.get(Q(name=request.GET['name'],
                                  workflow=tk.workflow) &
                                (Q(from_status=tk.status) |
                                 Q(from_status=None)))
    if tr is None:
        raise Http404('Not a valid transition for this ticket.')

    if not request.user.has_perm('projects.edit_content', tk.project):
        raise PermissionDenied

    tk.status = tr.to_status
    tk.save()

    fire_hooks(tr, tk)

    return redirect('/tickets/' + tk.key)


@login_required
@require_http_methods(['POST'])
def comment(request, key=''):
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('comments').\
        all()
    if len(t) == 0:
        raise Http404('No ticket with that key found.')

    if not request.user.has_perm('projects.comment_content', t.project):
        raise PermissionDenied

    c = Comment(body=request.POST['body'], author=request.user, ticket=t[0])
    c.save()

    return redirect('/tickets/' + t[0].key)


@login_required
@require_http_methods(['POST', 'DELETE'])
def edit_comment(request, id=0):
    c = Comment.objects.get(id=int(id))
    nxt = '/'

    if request.user != c.author and not request.user.is_staff:
            raise PermissionDenied

    if request.method == 'POST':
        if request.user != c.author and not request.user.is_staff:
            raise PermissionDenied
        c.body = request.POST['body']
        c.save()
        nxt = request.POST.get('next', nxt)
    else:
        c.delete()
    return redirect(nxt)


# TODO: Reduce the complexity and code duplication in this function.
@login_required
@require_http_methods(['GET', 'POST', 'DELETE'])
def edit_ticket(request, key=''):
    t = Ticket.objects.get(key=key)
    fs = FieldScheme.objects.\
        filter(project=t.project,
               ticket_type=t.ticket_type).\
        all()
    if len(fs) == 0:
        fs = FieldScheme.objects.\
            filter(project=t.project,
                   ticket_type=None).\
            all()

    def edit_form(error=None):
        field_scheme_fields = list(fs[0].fields.all())
        existing_fields = list(t.fields.all())
        existing_field_names = [f.name for f in existing_fields]
        return render(request, 'tickets/edit_ticket.html', {
            'error': error,
            'ticket': t,
            'fields': existing_fields + [f for f in field_scheme_fields
                                         if f.name not in existing_field_names]
        })

    if request.method == 'GET':
        if not request.user.has_perm('projects.edit_content', t.project):
            raise PermissionDenied
        return edit_form()
    elif request.method == 'DELETE':
        if not request.user.has_perm('projects.delete_content', t.project):
            raise PermissionDenied
        t.delete()
        return redirect('/')

    if not request.user.has_perm('projects.edit_content', t.project):
        raise PermissionDenied

    # Since we can have arbitrary custom fields extract all values into a
    # mutable dict
    fields = request.POST.copy()

    # Pop the defaults
    summary = fields.pop('summary', None)
    description = fields.pop('description', None)
    labels = fields.pop('label', None)
    assignee = fields.pop('assignee', None)
    reporter = fields.pop('reporter', None)

    if summary:
        t.summary = summary[0]

    if description:
        t.description = description[0]

    if labels:
        l = list(Label.objects.filter(name__in=labels).all())
        t.labels.set(l)

    if assignee:
        a = User.objects.get(username=assignee[0])
        t.assignee = a

    if reporter:
        a = User.objects.get(username=reporter[0])
        t.reporter = a

    print('yep')
    allowed_fields = [f.name for f in fs[0].fields.all()]
    for f, v in fields.items():
        print(f)
        print(v)
        if f == 'csrfmiddlewaretoken':
            continue
        if f not in allowed_fields:
            return edit_form('Field ' + f +
                             ' is not allowed for this Project and Ticket Type')
        try:
            fv = FieldValue.objects.get(ticket=t, field__name=f)
        except FieldValue.DoesNotExist:
            field = Field.objects.get(name=f)
            fv = FieldValue(field=field, ticket=t)
        fv.set_value(v)
        fv.save()

    t.save()
    return redirect('/tickets/' + t.key)


@login_required
@require_http_methods(['POST'])
def attachments(request, key=''):
    tk = Ticket.objects.get(key=key)
    AttachmentForm(request.POST, request.FILES)
    for f in request.FILES.getlist('attachment'):
        attachment = Attachment(name=f.name, attachment=f, ticket=tk, uploader=request.user)
        attachment.save()
    return redirect('/tickets/' + tk.key)
