"""Contains resources for interacting with labels."""

import praelatus.lib.labels as labels
from praelatus.api.schemas import LabelSchema
from praelatus.api.v1.base import BaseMultiResource
from praelatus.api.v1.base import BaseResource


class LabelsResource(BaseMultiResource):
    """Handlers for the /api/v1/labels endpoint."""
    schema = LabelSchema
    lib = labels


class LabelResource(BaseResource):
    """Handlers for the /api/v1/labels/{id} endpoint."""
    model_name = 'label'
    lib = labels
