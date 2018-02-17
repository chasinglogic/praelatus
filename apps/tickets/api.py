from rest_framework import generics

from .models import Comment, Ticket, TicketType
from .serializers import (CommentSerializer, TicketSerializer,
                          TicketTypeSerializer)


class TicketList(generics.ListCreateAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        projects = get_objects_for_user(self.request.user,
                                        'projects.view_project')
        q = Q()
        query = self.request.GET.get('query')
        if query is not None:
            try:
                q = compile_q(query)
            # Ignore the error in the API
            except CompileException:
                pass
        return Ticket.objects.\
            filter(project__in=projects).\
            prefetch_related('ticket_type').\
            prefetch_related('status').\
            prefetch_related('labels').\
            prefetch_related('fields').\
            prefetch_related('comments').\
            prefetch_related('links').\
            filter(q).\
            all()


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
