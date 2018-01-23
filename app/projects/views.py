# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import get_objects_for_user
from notifications.models import Notification
from rest_framework import generics
from tickets.models import Ticket
from django.contrib.auth.models import Permission, User
from guardian.shortcuts import remove_perm, assign_perm
from schemes.models import WorkflowScheme
from workflows.models import Workflow
from tickets.models import TicketType
from django.db import IntegrityError

from .models import Project
from .forms import ProjectForm
from .serializers import ProjectSerializer

from functools import wraps


def next(fn):
    """Redirect to query param next if present defaults to '/'."""

    @wraps(fn)
    def wrapper(request, **kwargs):
        res = fn(request, **kwargs)
        if res:
            return res

        if request.method == 'GET':
            nxt = request.GET.get('next', '/')
        elif request.method == 'POST':
            nxt = request.GET.get('next', '/')
        elif request.method == 'PUT':
            nxt = request.GET.get('next', '/')
        elif request.method == 'DELETE':
            nxt = request.GET.get('next', '/')
        else:
            nxt = '/'

        return redirect(nxt)

    return wrapper


def project_by_key(fn):
    """Get a project by key in the url, raise 404 if does not exist.

    Will pass project as the 'project' kwarg to the wrapped function.
    """

    @wraps(fn)
    def wrapper(request, key='', **kwargs):
        try:
            p = Project.objects.get(key=key)
        except Project.DoesNotExist:
            raise Http404()

        return fn(request, project=p, **kwargs)

    return wrapper


def project_permission_required(perm):
    """Verify that the request.user has the perm on the project."""

    def deco(fn):
        @project_by_key
        @wraps(fn)
        def wrapper(request, project=None, **kwargs):
            if not request.user.has_perm(perm, project):
                raise PermissionDenied()
            return fn(request, project=project, **kwargs)

        return wrapper

    return deco


class ProjectList(generics.ListCreateAPIView):
    """API for projects."""
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return get_objects_for_user(self.request.user, 'projects.view_project')


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'key'


# UI


@project_by_key
def show(request, project=None):
    """Show a single project"""
    activity = Notification.objects.\
        filter(target_object_id=project.id).\
        all()[:25]

    return render(request, 'projects/show.html',
                  {'project': project,
                   'open_query': 'project = "{}"'.format(project.key),
                   'activity': activity})


def search(request):
    q = Q()

    query = request.GET.get('query', '')
    if query == '':
        q = (Q(key__icontains=query) | Q(name__icontains=query)
             | Q(lead__username=query) | Q(lead__email=query)
             | Q(lead__first_name__icontains=query)
             | Q(lead__last_name__icontains=query))

    results = Project.objects.\
        prefetch_related('lead').\
        filter(q).\
        all()

    return render(request, 'projects/project_filter.html',
                  {'results': results})


editable_permissions = [
    'admin_project',
    'create_tickets',
    'edit_tickets',
    'delete_tickets',
    'add_comments',
    'view_project',
]


def admin(request, key=''):
    project = Project.objects.\
        prefetch_related('lead').\
        prefetch_related('groups').\
        prefetch_related('workflow_schemes').\
        prefetch_related('ticket_types').\
        filter(key=key)

    if len(project) == 0:
        raise Http404()
    elif not request.user.has_perm('projects.admin_project', project[0]):
        raise PermissionDenied()

    permissions = Permission.objects.filter(codename__in=editable_permissions)

    workflows = Workflow.objects.all()
    ticket_types = TicketType.objects.all()

    return render(request, 'projects/admin.html', {
        'project': project[0],
        'workflows': workflows,
        'ticket_types': ticket_types,
        'permissions': permissions,
    })


@project_permission_required('projects.admin_project')
def edit(request, project=None):
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        form.save()

        print(form.changed_data)

        if 'key' in form.changed_data:
            for t in Ticket.objects.filter(project=project):
                t.key = project.key + '-' + t.key.split('-')[1]
                t.save()
            return redirect('/projects/' + project.key + '/admin/edit')

    form = ProjectForm(instance=project)
    return render(request, 'projects/edit.html',
                  {'project': project,
                   'form': form})


@project_permission_required('projects.admin_project')
@next
def remove_workflow(request, project=None):
    ticket_type = request.GET.get('ticketType')
    if ticket_type:
        ws = WorkflowScheme.objects.filter(
            project=project, ticket_type__id=int(ticket_type))
        if len(ws) != 0:
            ws[0].delete()


@project_permission_required('projects.admin_project')
@next
def add_workflow(request, project=None):
    ticket_type = [int(i) for i in request.GET.getlist('ticketType')]
    workflow = request.GET.get('workflow')

    tt = TicketType.objects.\
        filter(id__in=ticket_type).distinct()
    w = Workflow.objects.filter(id=int(workflow))

    for typ in tt:
        ws = WorkflowScheme(project=project, workflow=w[0], ticket_type=typ)
        try:
            ws.save()
        except IntegrityError:
            pass

    # Check if we're trying to set the default.
    if 0 in ticket_type and len(w) != 0:
        print('setting default workflow')
        q = WorkflowScheme.objects.filter(project=project, ticket_type=None)

        if len(q) == 0:
            ws = WorkflowScheme(project=project, ticket_type=None)
        else:
            ws = q[0]

        ws.workflow = w[0]
        ws.save()


@project_permission_required('projects.admin_project')
@next
def edit_project_perm(request, op_fn=None, project=None):
    """Apply the appropriate guardian shortcut for each request."""
    perm_name = request.GET.get('permission')
    group_name = request.GET.get('group')

    if (perm_name and group_name) and perm_name in editable_permissions:
        g = project.groups.filter(name=group_name)
        if len(g) == 0:
            raise Http404()
        op_fn(perm_name, g[0], project)
        g[0].save()


def remove_permission(request, key=''):
    return edit_project_perm(request, key=key, op_fn=remove_perm)


def add_permission(request, key=''):
    return edit_project_perm(request, key=key, op_fn=assign_perm)


@project_permission_required('projects.admin_project')
@next
def remove_ticket_type(request, project=None):
    ticket_type = request.GET.get('ticketType')
    if ticket_type:
        tt = project.ticket_types.filter(id=int(ticket_type))
        if len(tt) != 0:
            project.ticket_types.remove(tt[0])
            project.save()


@project_permission_required('projects.admin_project')
@next
def add_ticket_type(request, project=None):
    typs = request.GET.getlist('ticketType')
    for t in typs:
        try:
            ttype = TicketType.objects.get(id=int(t))
        except TicketType.DoesNotExist:
            raise Http404('No Ticket Type with id ' + t + ' exists.')
        project.ticket_types.add(ttype)

    project.save()


@project_permission_required('projects.admin_project')
@next
def add_user_to_group(request, project=None):
    user_ids = [int(i) for i in request.GET.getlist('users')]
    group_id = int(request.GET.get('group', 0))

    users = User.objects.filter(id__in=user_ids)
    groups = project.groups.filter(id=group_id)
    if len(groups) != 0:
        group = groups[0]
        group.user_set = users
        group.save()


@project_permission_required('projects.admin_project')
@next
def remove_user_from_group(request, project=None):
    user_id = int(request.GET.get('user', 0))
    group_id = int(request.GET.get('group', 0))

    user = User.objects.filter(id=user_id)
    groups = project.groups.filter(id=group_id)
    if len(groups) != 0 and len(user) != 0:
        group = groups[0]
        group.user_set.remove(user[0])
        group.save()
