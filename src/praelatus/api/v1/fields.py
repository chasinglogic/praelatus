"""Contains resources for interacting with fields."""

import praelatus.lib.fields as fields

from praelatus.api.v1.base import BaseMultiResource
from praelatus.api.v1.base import BaseResource
from praelatus.api.schemas import FieldSchema
from praelatus.models.fields import FieldOption


class FieldsResource(BaseMultiResource):
    """Handlers for the /api/v1/fields endpoint."""
    schema = FieldSchema
    lib = fields


class FieldResource(BaseResource):
    """Handlers for the /api/v1/fields/{id} endpoint."""
    model_name = 'field'
    lib = fields
