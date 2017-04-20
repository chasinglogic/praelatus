"""Defines schema for ticket objects and related objects."""

from praelatus.api.schemas.base import BaseSchema


class StatusSchema(BaseSchema):
    """Used for validation of status objects."""
    pass


class TicketTypeSchema(BaseSchema):
    """Used for validation of ticket type objects."""
    pass


class TicketSchema(BaseSchema):
    """Used for validation of ticket objects."""
    schema = {
        'title': 'ticket',
        'type': 'object',
        'properties': {
            'id': {'type': 'integer'},
        }
    }
