from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import generics

from .models import Field, DataTypes
from .serializers import FieldSerializer


def data_types(request):
    return JsonResponse(DataTypes.values(), safe=False)


class FieldList(generics.ListCreateAPIView):
    """API for fields."""
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class FieldDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for fields."""
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
