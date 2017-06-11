from django.shortcuts import render
from .models import Project


def show(request, key=''):
    """Show a single project"""
    p = Project.objects.get(key=key)
    return render(request, 'projects/show.html', {
        'project': p,
        'content': p.content.all()
    })


def search(request):
    """Search through projects."""
    q = request.GET.get('filter', '')

    if q == '':
        projects = Project.objects.all()
    elif ':' in q:
        split = q.split(' ')
        projects = Project.objects.\
            filter(**{s.split(':')[0]: s.split(':')[1] for s in split}).\
            all()
    else:
        projects = Project.objects.filter(key=q).all()

    return render(request, 'projects/search.html', {'projects': projects})
