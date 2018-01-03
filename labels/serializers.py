from rest_framework import serializers

from .models import Label


class LabelSerializer(serializers.ModelSerializer):
    """Serialize a label to JSON."""

    class Meta:
        model = Label
        fields = (
            'id',
            'name',
            'bg_color'
        )
