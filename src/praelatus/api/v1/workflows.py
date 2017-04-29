"""Contains resources for interacting with workflows."""

import json
import falcon

import praelatus.lib.statuses as statuses
import praelatus.lib.workflows as workflows

from praelatus.lib import session
from praelatus.api.schemas import WorkflowSchema


class WorkflowsResource():
    """Handlers for the /api/v1/workflows endpoint."""

    def on_post(self, req, resp):
        """
        Create a new workflow and return the new workflow object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-workflows
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        WorkflowSchema.validate(jsn)
        with session() as db:
            db_res = workflows.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all workflows the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available workflows.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-workflows
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = workflows.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class WorkflowResource():
    """Handlers for the /api/v1/workflows/{id} endpoint."""

    def on_get(self, req, resp, id):
        """
        Get a single workflow by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-workflowsid
        """
        user = req.context['user']
        with session() as db:
            db_res = workflows.get(db, actioning_user=user, id=id)
            if db_res is None:
                raise falcon.HTTPNotFound()
            resp.body = db_res.to_json()

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

        resp.body = json.dumps({'message': 'Successfully update workflow.'})

    def on_delete(self, req, resp, id):
        """
        Update the workflow indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-workflowsid
        """
        user = req.context['user']
        with session() as db:
            db_res = workflows.get(db, actioning_user=user, id=id)
            workflows.delete(db, actioning_user=user, workflow=db_res)

        resp.body = json.dumps({'message': 'Successfully deleted workflow.'})
