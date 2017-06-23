from fields.serializers import FieldValueSerializer
from labels.serializers import LabelSerializer
from projects.serializers import ProjectSerializer, UserSerializer
from rest_framework import serializers
from workflows.serializers import TransitionSerializer

from .models import Comment, Ticket, TicketType


class CommentSerializer(serializers.ModelSerializer):
    """Serialize a ticket type to JSON."""
    author = UserSerializer()

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'author',
            'created_at',
            'updated_at'
        )


class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = (
            'id',
            'name'
        )


class TicketSerializer(serializers.ModelSerializer):
    labels = LabelSerializer(many=True)
    fields = FieldValueSerializer(many=True)
    transitions = TransitionSerializer(many=True)
    assignee = UserSerializer()
    reporter = UserSerializer()
    project = ProjectSerializer()
    ticket_type = TicketTypeSerializer()

    class Meta:
        model = Ticket
        fields = (
            'id',
            'key',
            'updated_at',
            'created_at',
            'summary',
            'description',
            'ticket_type',
            'labels',
            'fields',
            'assignee',
            'reporter',
            'project',
            'transitions'
        )
