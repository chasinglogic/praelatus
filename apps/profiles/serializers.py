from django.contrib.auth.models import User

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serialize a django.contrib.auth.models.User to JSON."""

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')
