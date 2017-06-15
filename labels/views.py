from rest_framework import generics
from rest_framework import filters

from .models import Label
from .serializers import LabelSerializer


class LabelList(generics.ListCreateAPIView):
    """API for labels."""
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for labels."""
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
