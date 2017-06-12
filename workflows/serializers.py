from rest_framework import serializers

from .models import Workflow, Status, Transition


class StatusSerializer(serializers.ModelSerializer):
    """Serialize a status to JSON."""

    class Meta:
        model = Status
        fields = (
            'id',
            'name',
        )


class TransitionSerializer(serializers.ModelSerializer):
    """Serialize a transition to JSON."""
    from_status = StatusSerializer()
    to_status = StatusSerializer()

    class Meta:
        model = Transition
        fields = (
            'id',
            'name',
            'from_status',
            'to_status'
        )


class WorkflowSerializer(serializers.ModelSerializer):
    """Serialize a workflow to JSON."""
    transitions = TransitionSerializer(many=True)

    class Meta:
        model = Workflow
        fields = (
            'id',
            'name',
            'transitions'
        )
