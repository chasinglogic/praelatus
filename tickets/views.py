from django.shortcuts import render, redirect
from django.http import Http404

from rest_framework import generics

from workflows.tasks import fire_hooks
from workflows.models import Transition
from .models import Comment, Ticket, TicketType
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


def dashboard(request):
    return render(request, 'dashboard/index.html')


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

    fire_hooks(tr, t)

    return redirect('/tickets/' + t.key)
