from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import Status, Transition, Workflow
from .serializers import (StatusSerializer, TransitionSerializer,
                          WorkflowSerializer)


class WorkflowList(generics.ListCreateAPIView):
    """API for workflows."""
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (IsAdminUser,)


class WorkflowDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for workflows."""
    queryset = Workflow.objects.all()
    serializer_class = WorkflowSerializer
    permission_classes = (IsAdminUser,)


class TransitionList(generics.ListCreateAPIView):
    """API for transitions."""
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    permission_classes = (IsAdminUser,)


class TransitionDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for transitions."""
    queryset = Transition.objects.all()
    serializer_class = TransitionSerializer
    permission_classes = (IsAdminUser,)


class StatusList(generics.ListCreateAPIView):
    """API for statuss."""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)


class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    """API for statuss."""
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = (IsAdminUser,)
