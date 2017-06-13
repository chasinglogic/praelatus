from django.shortcuts import render

from .models import Project
from .serializers import ProjectSerializer
from rest_framework import generics

# API


class ProjectList(generics.ListCreateAPIView):
    """API for projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for projects."""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    lookup_field = 'key'

# UI


def show(request, key=''):
    """Show a single project"""
    p = Project.objects.get(key=key)
    return render(request, 'projects/show.html', {
        'project': p,
        'content': p.content.all()
    })
