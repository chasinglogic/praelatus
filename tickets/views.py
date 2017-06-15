from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from fields.models import Field, FieldValue
from projects.models import Project
from rest_framework import generics
from workflows.models import Transition
from workflows.tasks import fire_hooks

from .models import Comment, FieldScheme, Ticket, TicketType
from .serializers import (CommentSerializer, TicketSerializer,
                          TicketTypeSerializer)

# API


class TicketList(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


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
    return render(request, 'tickets/show.html', {'ticket': t[0]})


@login_required
def create(request, project_key='', ticket_type=''):
    if not request.user.is_authenticated():
        return redirect('/login?next=' + request.path)

    if request.method == 'POST':
        proj = Project.objects.get(key=project_key)
        ttype = TicketType.objects.get(name=ticket_type)

        workflows = proj.workflow_schemes.filter(ticket_type=ttype).all()
        if len(workflows) == 0:
            # Get the default workflow
            workflow = proj.workflow_schemes.\
                       filter(ticket_type=None).all()[0].workflow
        else:
            workflow = workflows[0].workflow

        create = workflow.transitions.filter(name='Create').all()[0]

        t = Ticket(
            key=project_key + '-' + str(proj.content.count() + 1),
            summary=request.POST['summary'],
            project=proj,
            reporter=request.user,
            ticket_type=ttype,
            status=create.to_status,
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
        filter(project__key=project_key,
               ticket_type__name=ticket_type).\
        all()

    if len(fs) == 0:
        fs = FieldScheme.objects.\
            filter(project__key=project_key,
                   ticket_type=None).\
            all()

    return render(request, 'tickets/create.html', {'fs': fs[0]})


def create_prompt(request):
    projects = Project.objects.all()
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
    tr = Transition.objects.get(name=request.GET['name'],
                                from_status=tk.status,
                                workflow=tk.workflow)
    if tr is None:
        raise Http404('Not a valid transition for this ticket.')

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

    c = Comment(body=request.POST['body'], author=request.user, ticket=t[0])
    c.save()

    return redirect('/tickets/' + t[0].key)



@login_required
@require_http_methods(['POST', 'DELETE'])
def edit_comment(request, id=0):
    c = Comment.objects.get(id=int(id))
    nxt = '/'
    if request.method == 'POST':
        c.body = request.POST['body']
        c.save()
        nxt = request.POST.get('next', nxt)
    else:
        c.delete()
    return redirect(nxt)
