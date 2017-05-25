"""Defines schema for project objects."""

from praelatus.app.api.schemas.base import BaseSchema
from praelatus.app.api.schemas.user import UserSchema


class ProjectSchema(BaseSchema):
    """Used for validation of project objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'repo': {'type': ['string', 'null']},
            'homepage': {'type': ['string', 'null']},
            'icon_url': {'type': ['string', 'null']},
            'description': {'type': 'string'},
            'key': {'type': 'string'},
            'lead': UserSchema.schema
        },
        'required': ['name', 'key', 'lead']
    }
