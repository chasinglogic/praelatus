"""Defines schema for workflow objects and related objects."""

from praelatus.api.schemas.base import BaseSchema


class StatusSchema(BaseSchema):
    """Used for validation of status objects."""
    pass


class HookSchema(BaseSchema):
    """Used for validation of hook objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {'type': 'string'},
            'description': {'type': 'string'},
            'body': {'type': 'string'},
            'url': {'type': 'string'},
            'method': {'type': 'string'}
        },
        'required': ['name', 'body', 'method']
    }


class TransitionSchema(BaseSchema):
    """Used for validation of transition objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {
                'type': 'string',
                'maxLength': 250
            },
            'from_status': StatusSchema.schema,
            'to_status': StatusSchema.schema,
            'hooks': {
                'type': 'array',
                'items': HookSchema.schema
            }
        }
    }


class WorkflowSchema(BaseSchema):
    """Used for validation of workflow objects."""
    schema = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
            'name': {
                'type': 'string',
                'maxLength': 250
            },
            'description': {'type': ['string', 'null']},
            'transitions': {
                'type': 'object',
                'patternProperties': {
                    '.*': {
                        'type': 'array',
                        'items': TransitionSchema.schema
                    }
                }
            }
        }
    }
