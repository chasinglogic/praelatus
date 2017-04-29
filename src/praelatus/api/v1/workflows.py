"""Contains resources for interacting with workflows."""

import json

import praelatus.lib.workflows as workflows

from praelatus.lib import session
from praelatus.api.schemas import WorkflowSchema
from praelatus.api.v1.base import BaseResource
from praelatus.api.v1.base import BaseMultiResource


class WorkflowsResource(BaseMultiResource):
    """Handlers for the /api/v1/workflows endpoint."""
    schema = WorkflowSchema
    lib = workflows


class WorkflowResource(BaseResource):
    """Handlers for the /api/v1/workflows/{id} endpoint."""
    model_name = 'workflow'
    lib = workflows

    def on_put(self, req, resp, id):
        """
        Update the workflow indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-workflowsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = workflows.get(db, actioning_user=user, id=id)
            updated = workflows.update_from_json(db, db_res, jsn,
                                                 actioning_user=user)
            workflows.update(db, actioning_user=user, workflow=updated)

        resp.body = json.dumps({'message': 'Successfully updatedd workflow.'})
