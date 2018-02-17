from profiles.serializers import UserSerializer
from projects.serializers import ProjectSerializer
from rest_framework import serializers
from tickets.serializers import TicketSerializer

from .models import Activity, Notification


class ActivitySerializer(serializers.ModelSerializer):
    """Serialize an activity into JSON"""

    actioning_user = UserSerializer()
    project = ProjectSerializer()
    ticket = TicketSerializer()

    class Meta:
        model = Activity
        fields = ('id', 'actioning_user', 'type',
                  'ticket', 'project', 'timestamp')


class NotificationSerializer(serializers.ModelSerializer):

    activity = ActivitySerializer()

    class Meta:
        model = Notification
        fields = ('id', 'activity', 'body', 'acknowledged', 'sent')
