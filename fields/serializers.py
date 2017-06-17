from rest_framework import serializers

from .models import Field, FieldOption, FieldValue


class FieldOptionSerializer(serializers.ModelSerializer):
    """Serialize a field option to JSON."""

    class Meta:
        model = FieldOption
        fields = (
            'id',
            'name',
        )


class FieldSerializer(serializers.ModelSerializer):
    """Serialize a field to JSON."""
    options = FieldOptionSerializer

    class Meta:
        model = Field
        fields = (
            'id',
            'name',
            'data_type',
            'options'
        )


class FieldValueSerializer(serializers.ModelSerializer):
    """Serialize a field to JSON."""
    options = FieldOptionSerializer(many=True)

    class Meta:
        model = FieldValue
        fields = (
            'id',
            'name',
            'data_type',
            'options',
            'value'
        )
