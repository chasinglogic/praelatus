"""Defines schema for workflow objects and related objects."""

from praelatus.api.schemas.base import BaseSchema


class PermissionSchemeSchema(BaseSchema):
    """Used for validation of PermissionScheme objects."""
    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'permissions': {
                'type': 'object',
                'patternProperties': {
                    '.*': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    }
                }
            },
        }
    }
