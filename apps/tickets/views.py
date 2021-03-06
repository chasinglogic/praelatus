# import the logging library
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

import markdown
from fields.models import Field, FieldValue
from guardian.shortcuts import get_objects_for_user
from labels.models import Label
from notifications.models import Activity
from notifications.tasks import notify_watchers
from projects.models import Project
from queries.dsl import CompileException, compile_q
from schemes.models import FieldScheme, WorkflowScheme
from workflows.models import Transition
from workflows.tasks import fire_web_hooks

from .forms import AttachmentForm
from .models import Attachment, Comment, Ticket, TicketType
from .models.links import Link
from .models.upvotes import Upvote

# Get an instance of a logger
logger = logging.getLogger(__name__)


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
def create(request):
    flash = None

    if request.method == 'POST':
        proj = Project.objects.get(id=request.POST.get('project'))
        if not request.user.has_perm('projects.create_tickets', proj):
            raise PermissionDenied

        ttype = TicketType.objects.get(id=request.POST.get('ticket_type'))
        workflow = WorkflowScheme.\
            get_for_project(project=proj, ticket_type=ttype).\
            workflow

        task_of = request.POST.get('task_of')
        parent = Ticket.objects.get(id=task_of) if task_of else None

        t = Ticket(
            key=proj.key + '-' + str(proj.content.count() + 1),
            summary=request.POST['summary'],
            project=proj,
            reporter=request.user,
            ticket_type=ttype,
            status=workflow.create_status,
            workflow=workflow,
            description=request.POST['description'])

        if parent:
            t.parent = parent

        t.save()

        fields = [
            f for f in request.POST.keys()
            if (f != 'labels' and f != 'summary' and f != 'description'
                and f != 'csrfmiddlewaretoken' and f != 'project'
                and f != 'ticket_type' and f != 'task_of')
        ]

        for f in fields:
            field = Field.objects.get(name=f)
            value = FieldValue(field=field, content_object=t)
            value.set_value(request.POST[f])
            value.save()
        return redirect('/tickets/' + t.key)

    # Grab the params
    project = request.GET.get('project')
    ticket_type = request.GET.get('ticket_type')

    p = Project.objects.get(id=project) if project else None
    if p and not request.user.has_perm('projects.create_tickets', p):
        flash = 'You do not have permission to create tickets in this project.'

    tt = TicketType.objects.get(id=ticket_type) if ticket_type else None

    fs = FieldScheme.get_for_project(project=p, ticket_type=tt) \
        if project and ticket_type else None

    return render(request, 'tickets/create.html',
                  {
                      'fs': fs,
                      'projects': Project.objects.all(),
                      'ticket_type': tt,
                      'project': p,
                      'flash_message': flash,
                      'task': request.GET.get('task_of')
                  })


@login_required
def dashboard(request):
    notifications = request.user.notifications.\
        filter(Q(acknowledged=False)).\
        order_by('-sent'). \
        all()[:50]
    reported = request.user.reported.\
        filter(~Q(status__state='DONE')).\
        all()[:10]
    assigned = request.user.assigned.\
        filter(~Q(status__state='DONE')).\
        all()[:10]
    projects = request.user.projects.all()[:10]

    return render(request, 'tickets/dashboard.html',
                  {
                      'notifications': notifications,
                      'assigned': assigned,
                      'reported': reported,
                      'projects': projects
                  })


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

    Activity(
        project=tk.project,
        content_object=tr,
        ticket=tk,
        actioning_user=request.user,
        type=Activity.Transition
    ).save()

    return redirect('/tickets/' + tk.key)


@login_required
@require_http_methods(['POST'])
def comment(request, key=''):
    t = Ticket.objects.\
        filter(key=key).\
        prefetch_related('project').\
        prefetch_related('watchers').\
        prefetch_related('comments').\
        first()
    if t is None:
        raise Http404('No ticket with that key found.')

    if not request.user.has_perm('projects.add_comments', t.project):
        raise PermissionDenied

    c = Comment(body=request.POST['body'], author=request.user, ticket=t)
    c.save()

    return redirect('/tickets/' + t.key + '#comment-form')


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
        label_list = list(Label.objects.filter(name__in=labels).all())
        t.labels.set(label_list)

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

    Link(
        owner=request.user,
        display=request.POST['display'],
        href=request.POST['url'],
        content_object=tk
    ).save()

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
