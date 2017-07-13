from django.db.models import Q
from django.shortcuts import render
from guardian.shortcuts import get_objects_for_user
from notifications.models import Notification
from rest_framework import generics

from .models import Project
from .serializers import ProjectSerializer

# API


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


def show(request, key=''):
    """Show a single project"""
    p = Project.objects.get(key=key)
    activity = Notification.objects.\
        filter(target_object_id=p.id).\
        all()[:25]

    return render(request, 'projects/show.html', {
        'project': p,
        'activity': activity
    })


def search(request):
    q = Q()

    query = request.GET.get('query', '')
    if query == '':
        q = (Q(key__icontains=query) |
             Q(name__icontains=query) |
             Q(lead__username=query) |
             Q(lead__email=query) |
             Q(lead__first_name__icontains=query) |
             Q(lead__last_name__icontains=query))

    results = Project.objects.\
        prefetch_related('lead').\
        filter(q).\
        all()

    return render(request,
                  'projects/project_filter.html',
                  {'results': results})
