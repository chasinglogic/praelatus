"""Contains resources for interacting with labels."""

import json
import falcon

import praelatus.lib.labels as labels

from praelatus.lib import session
from praelatus.api.schemas import LabelSchema


class LabelsResource():
    """Handlers for the /api/v1/labels endpoint."""

    def on_post(self, req, resp):
        """Create a new label and return the new label object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-labels
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        LabelSchema.validate(jsn)
        with session() as db:
            db_res = labels.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """Get all labels the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available labels.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-labels
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = labels.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class LabelResource():
    """Handlers for the /api/v1/labels/{id} endpoint."""

    def on_get(self, req, resp, id):
        """Get a single label by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-labelsid
        """
        user = req.context['user']
        with session() as db:
            db_res = labels.get(db, actioning_user=user, id=id)
            if db_res is None:
                raise falcon.HTTPNotFound()
            resp.body = db_res.to_json()

    def on_put(self, req, resp, id):
        """Update the label indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-labelsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = labels.get(db, actioning_user=user, id=id)
            db_res.name = jsn['name']
            labels.update(db, actioning_user=user, label=db_res)

        resp.body = json.dumps({'message': 'Successfully update label.'})

    def on_delete(self, req, resp, id):
        """Update the label indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-labelsid
        """
        user = req.context['user']
        with session() as db:
            db_res = labels.get(db, actioning_user=user, id=id)
            labels.delete(db, actioning_user=user, label=db_res)

        resp.body = json.dumps({'message': 'Successfully deleted label.'})
