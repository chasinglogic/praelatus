"""Contains resources for interacting with statuses."""

import praelatus.lib.statuses as statuses

from praelatus.api.schemas import StatusSchema
from praelatus.api.v1.base import BaseMultiResource
from praelatus.api.v1.base import BaseResource


class StatusesResource(BaseMultiResource):
    """Handlers for the /api/v1/statuses endpoint."""
    schema = StatusSchema
    lib = statuses


class StatusResource(BaseResource):
    """Handlers for the /api/v1/statuses/{id} endpoint."""
    model_name = 'status'
    lib = statuses
