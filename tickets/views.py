from django.shortcuts import render

from rest_framework import generics

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
        prefetch_related('labels').\
        prefetch_related('fields').\
        prefetch_related('comments').\
        all()

    if len(t) == 0:
        return render(request, '404.html',
                      {'message': 'No ticket with that key found.'})
    return render(request, 'tickets/show.html', {'ticket': t[0]})



def dashboard(request):
    return render(request, 'dashboard/index.html')
