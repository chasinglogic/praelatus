from rest_framework import generics

from .models import Label
from .serializers import LabelSerializer


class LabelList(generics.ListCreateAPIView):
    """API for labels."""
    queryset = Label.objects.all()
    serializer_class = LabelSerializer


class LabelDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for labels."""
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
