from django.http import JsonResponse
from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import DataTypes, Field
from .serializers import FieldSerializer


def data_types(request):
    return JsonResponse(DataTypes.values(), safe=False)


class FieldList(generics.ListCreateAPIView):
    """API for fields."""
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = (IsAdminUser,)


class FieldDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for fields."""
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = (IsAdminUser,)
