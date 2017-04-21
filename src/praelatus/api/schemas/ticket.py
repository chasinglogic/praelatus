"""Defines schema for ticket objects and related objects."""

from praelatus.api.schemas.base import BaseSchema
from praelatus.api.schemas.user import UserSchema
from praelatus.api.schemas.project import ProjectSchema
from praelatus.api.schemas.workflow import TransitionSchema
from praelatus.api.schemas.workflow import StatusSchema


class LabelSchema(BaseSchema):
    """Used for validation of label objects."""
    pass


class TicketTypeSchema(BaseSchema):
    """Used for validation of ticket type objects."""
    pass


class FieldSchema(BaseSchema):
    """Used for validation of field objects."""
    pass


class FieldValueSchema(BaseSchema):
    """Used for validation of field value objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {
                'type': 'string',
                'maxLength': 250
            },
            'value': {
                'type': ['string', 'number']
            }
        }
    }


class CommentSchema(BaseSchema):
    """Used for validation of comment objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'author': UserSchema.schema,
            'updated_date': {
                'type': 'string',
                'format': 'date'
            },
            'created_date': {
                'type': 'string',
                'format': 'date'
            },
            'body': {'type': 'string'}
        }
    }


class TicketSchema(BaseSchema):
    """Used for validation of ticket objects."""
    schema = {
        'title': 'ticket',
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'summary': {
                'type': 'string',
                'maxLength': 250
            },
            'updated_date': {
                'type': 'string',
                'format': 'date'
            },
            'created_date': {
                'type': 'string',
                'format': 'date'
            },
            'description': {'type': 'string'},
            'labels': {
                'type': 'array',
                'items': {'type': 'string'}
            },
            'assignee': UserSchema.schema,
            'reporter': UserSchema.schema,
            'ticket_type': TicketTypeSchema.schema,
            'fields': {
                'type': 'array',
                'items': FieldValueSchema.schema
            },
            'comments': {
                'type': 'array',
                'items': CommentSchema.schema
            },
            'transitions': {
                'type': 'array',
                'items': TransitionSchema.schema
            },
            'key': {'type': 'string'},
            'status': StatusSchema.schema,
            'project': ProjectSchema.schema
        },
        'required': [
            'summary',
            'description',
            'fields',
            'reporter',
            'ticket_type',
            'project'
        ]
    }
