"""Defines schema for permission schemes and related objects."""

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


class RoleSchema(BaseSchema):
    """Used for validation of role objects."""
    pass
