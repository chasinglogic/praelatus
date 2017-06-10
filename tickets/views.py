from django.shortcuts import render


def show(request, key=''):
    """Show a single Ticket."""
    return render(request, 'tickets/show.html')
