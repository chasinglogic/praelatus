import markdown
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from guardian.shortcuts import get_objects_for_user
from notifications.signals import notify
from rest_framework import generics

from fields.models import Field, FieldValue
from hooks.tasks import fire_web_hooks
from labels.models import Label
from projects.models import Project
from workflows.models import Transition

from .forms import AttachmentForm
from schemes.models import FieldScheme, WorkflowScheme
from upvotes.models import Upvote
from links.models import Link
from .models import (Attachment, Comment, Ticket, TicketType)
from queries.dsl import CompileException, compile_q
from .serializers import (CommentSerializer, TicketSerializer,
                          TicketTypeSerializer)

# API


class TicketList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        projects = get_objects_for_user(self.request.user,
                                        'projects.view_project')
        q = Q()
        query = self.request.GET.get('query')
        if query is not None:
            try:
                q = compile_q(query)
            # Ignore the error in the API
            except CompileException:
                pass
        return Ticket.objects.\
            filter(project__in=projects).\
            prefetch_related('ticket_type').\
            prefetch_related('status').\
            prefetch_related('labels').\
            prefetch_related('fields').\
            prefetch_related('comments').\
            prefetch_related('links').\
            filter(q).\
            all()


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
        prefetch_related('links').\
        all()

    if (len(t) == 0 or
            not request.user.has_perm('projects.view_project', t[0].project)):
        raise Http404('No ticket with that key found.')

    attachment_form = AttachmentForm()
    return render(request, 'tickets/show.html',
                  {'ticket': t[0],
                   'attachment_form': attachment_form})


@login_required
def create(request, project_key='', ticket_type=''):
    proj = Project.objects.get(key=project_key)
    if not request.user.has_perm('projects.create_tickets', proj):
        raise PermissionDenied

    if request.method == 'POST':
        ttype = TicketType.objects.get(name=ticket_type)
        workflow = WorkflowScheme.\
            get_for_project(project=proj, ticket_type=ttype).\
            workflow

        t = Ticket(
            key=project_key + '-' + str(proj.content.count() + 1),
            summary=request.POST['summary'],
            project=proj,
            reporter=request.user,
            ticket_type=ttype,
            status=workflow.create_status,
            workflow=workflow,
            description=request.POST['description'])

        t.save()

        fields = [
            f for f in request.POST.keys()
            if (f != 'labels' and f != 'summary' and f != 'description'
                and f != 'csrfmiddlewaretoken')
        ]

        for f in fields:
            field = Field.objects.get(name=f)
            value = FieldValue(field=field, content_object=t)
            value.set_value(request.POST[f])
            value.save()

        return redirect('/tickets/' + t.key)

    fs = FieldScheme.get_for_project(
        project=proj, ticket_type__name=ticket_type)
    return render(request, 'tickets/create.html', {'fs': fs})


def create_prompt(request):
    projects = get_objects_for_user(request.user, 'projects.create_content')
    ticket_types = TicketType.objects.all()
    return render(request, 'tickets/create_prompt.html',
                  {'projects': projects,
                   'ticket_types': ticket_types})


@login_required
def notifications(request):
    notifications = request.user.notifications.\
        prefetch_related('action_object').\
        prefetch_related('target').\
        prefetch_related('actor').\
        all()
    return render(request, 'dashboard/notifications.html',
                  {'notifications': notifications})


@login_required
def reported(request):
    reported = request.user.reported.filter(~Q(status__state='DONE')).all()
    return render(request, 'dashboard/reported.html', {'reported': reported})


@login_required
def assigned(request):
    assigned = request.user.assigned.filter(~Q(status__state='DONE')).all()
    return render(request, 'dashboard/assigned.html', {'assigned': assigned})


@login_required
def transition(request, key=''):
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('status').\
        all()
    if len(t) == 0:
        raise Http404('No ticket with that key found.')

    tk = t[0]
    tr = Transition.objects.get(
        Q(name=request.GET['name'], workflow=tk.workflow) &
        (Q(from_status=tk.status) | Q(from_status=None)))
    if tr is None:
        raise Http404('Not a valid transition for this ticket.')

    if not request.user.has_perm('projects.edit_tickets', tk.project):
        raise PermissionDenied

    tk.status = tr.to_status
    tk.save()

    if len(tr.web_hooks.all()) > 0:
        fire_web_hooks.delay(tr.web_hooks.all(),
                             {'ticket': TicketSerializer(tk).data})

    notify.send(
        request.user,
        recipient=t[0].watching(),
        verb='transitioned to ' + tk.status.name,
        action_object=tk,
        target=tk.project)

    return redirect('/tickets/' + tk.key)


@login_required
@require_http_methods(['POST'])
def comment(request, key=''):
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('watchers').\
        prefetch_related('comments').\
        all()
    if len(t) == 0:
        raise Http404('No ticket with that key found.')

    if not request.user.has_perm('projects.add_comments', t[0].project):
        raise PermissionDenied

    c = Comment(body=request.POST['body'], author=request.user, ticket=t[0])
    c.save()

    notify.send(
        request.user,
        recipient=t[0].watching(),
        verb='commented on',
        action_object=t[0],
        target=t[0].project,
        description=markdown.markdown(c.body, safe_mode='escape'))

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


@login_required
@require_http_methods(['GET', 'POST', 'DELETE'])
def edit_ticket(request, key=''):
    t = Ticket.objects.get(key=key)
    fs = FieldScheme.get_for_project(t.project, ticket_type=t.ticket_type)

    def edit_form(error=None):
        field_scheme_fields = list(fs.fields.all())
        existing_fields = list(t.fields.all())
        # We have to check against names here since existing_fields is
        # actually a list of FieldValue's and not Field's
        existing_field_names = [f.name for f in existing_fields]
        return render(request, 'tickets/edit_ticket.html', {
            'error':
            error,
            'ticket':
            t,
            'fields':
            existing_fields + [
                f for f in field_scheme_fields
                if f.name not in existing_field_names
            ]
        })

    if request.method == 'DELETE':
        if not request.user.has_perm('projects.delete_tickets', t.project):
            raise PermissionDenied
        t.delete()
        return redirect('/')

    if not request.user.has_perm('projects.edit_tickets', t.project):
        raise PermissionDenied

    if request.method == 'GET':
        return edit_form()

    # Since we can have arbitrary custom fields extract all values into a
    # mutable dict
    fields = request.POST.copy()

    # Pop the defaults
    summary = fields.pop('summary', None)
    description = fields.pop('description', None)
    labels = fields.pop('label', None)
    assignee = fields.pop('assignee', None)

    if summary:
        t.summary = summary[0]

    if description:
        t.description = description[0]

    # TODO: Add this to the edit form.
    if assignee:
        a = User.objects.get(username=assignee[0])
        t.assignee = a

    # TODO: Add this to the edit form.
    if labels:
        l = list(Label.objects.filter(name__in=labels).all())
        t.labels.set(l)

    # Remove csrf token as we don't need it
    fields.pop('csrfmiddlewaretoken', None)

    allowed_fields = [f.name for f in fs.fields.all()]
    for f, v in fields.items():
        # Make sure they aren't doing anything malicious
        if f not in allowed_fields:
            return edit_form(
                'Field ' + f +
                ' is not allowed for this Project and Ticket Type')

        # Try to pull the existing value to update
        try:
            fv = FieldValue.objects.get(ticket=t, field__name=f)
        # If it doesn't exist then it's a new field so create it
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

    # Populate request.FILES
    AttachmentForm(request.POST, request.FILES)

    for f in request.FILES.getlist('attachment'):
        attachment = Attachment(
            name=f.name, attachment=f, ticket=tk, uploader=request.user)

        attachment.save()

    return redirect('/tickets/' + tk.key)


@login_required
@require_http_methods(['POST'])
def add_link(request, key=''):
    tk = Ticket.objects.get(key=key)

    link = Link(
        owner=request.user,
        display=request.POST['display'],
        href=request.POST['url'],
        content_object=tk)

    link.save()
    return redirect('/tickets/' + tk.key)


@login_required
@require_http_methods(['POST'])
def upvote(request, key=''):
    tk = Ticket.objects.get(key=key)

    q = Upvote.objects.filter(voter=request.user, ticket=tk).all()

    if len(q) == 0:
        u = Upvote(voter=request.user, content_object=tk)
        u.save()

    return redirect("/tickets/" + key)
