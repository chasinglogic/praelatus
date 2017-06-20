from rest_framework import serializers

from .models import Project, User


class UserSerializer(serializers.ModelSerializer):
    """Serialize a django.contrib.auth.models.User to JSON."""

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email'
        )


class ProjectSerializer(serializers.ModelSerializer):
    """Serialize a project as JSON."""
    lead = UserSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'name',
            'description',
            'lead',
            'icon',
            'homepage',
            'repo'
        )
