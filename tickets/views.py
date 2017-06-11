from django.shortcuts import render
from .models import Ticket


def show(request, key=''):
    """Show a single Ticket."""
    t = Ticket.objects.get(key=key)
    return render(request, 'tickets/show.html', {'ticket': t})
