"""Contains resources for interacting with self.lib."""

import json
import falcon

from praelatus.lib import session
from praelatus.api.schemas.base import BaseSchema


class BaseMultiResource():
    """A basic resource class that can handle the modelNames endpoints."""
    schema = BaseSchema
    lib = None

    def on_post(self, req, resp):
        """
        Create a new model and return the new model object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(jsn)
        with session() as db:
            db_res = self.lib.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all of the correct model the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available self.lib.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class BaseResource():
    """Handlers for the /api/v1/models/{id} endpoint."""
    model_name = 'base'
    lib = None

    def on_get(self, req, resp, id):
        """
        Get a single model by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-modelsid
        """
        user = req.context['user']
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, id=id)
            if db_res is None:
                raise falcon.HTTPNotFound()
            resp.body = db_res.to_json()

    def on_put(self, req, resp, id):
        """
        Update the model indicated by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, id=id)
            db_res.name = jsn['name']
            kwa = {}
            kwa[self.model_name] = db_res
            self.lib.update(db, actioning_user=user, **kwa)

        resp.body = json.dumps({
            'message': 'Successfully updated %s.' % self.model_name
        })

    def on_delete(self, req, resp, id):
        """
        Update the model indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelsid
        """
        user = req.context['user']
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, id=id)
            kwa = {}
            kwa[self.model_name] = db_res
            self.lib.delete(db, actioning_user=user, **kwa)

        resp.body = json.dumps({
            'message': 'Successfully deleted %s.' % self.model_name
        })
