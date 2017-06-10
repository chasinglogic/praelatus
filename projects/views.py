from django.shortcuts import render
from .models import Project


def show(request, key=''):
    """Show a single project"""
    p = Project.objects.get(key=key)
    return render(request, 'projects/show.html', {'project': p})
