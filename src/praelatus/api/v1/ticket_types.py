"""Contains resources for interacting with ticket_types."""

import praelatus.lib.ticket_types as ticket_types

from praelatus.api.schemas import TicketTypeSchema
from praelatus.api.v1.base import BaseMultiResource
from praelatus.api.v1.base import BaseResource


class TicketTypesResource(BaseMultiResource):
    """Handlers for the /api/v1/ticketTypes endpoint."""
    schema = TicketTypeSchema
    lib = ticket_types


class TicketTypeResource(BaseResource):
    """Handlers for the /api/v1/ticketTypes/{id} endpoint."""
    model_name = 'ticket_type'
    lib = ticket_types
