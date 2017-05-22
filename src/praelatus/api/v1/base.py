"""Contains resources for interacting with self.store."""

import json
import falcon

from praelatus.lib import session


class BaseResource:
    """A base class that just stores a schema and storage interface."""

    def __init__(self, store, schema):
        """Set the store module and json schema for this resource.

        If model_name is not provided it will be inferred from the
        module name of store. This works for most models as the plural
        is simply the model name + 's' the only exception being
        statuses.
        """
        self.schema = schema
        self.store = store
        self.model_name = store.__class__.__name__[:len("Store") * -1].lower()


class SearchResource(BaseResource):
    """A basic resource for providing a search enpoint."""

    def on_get(self, req, res):
        """Get all of the correct model the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available self.store.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = self.store.search(db, actioning_user=user, search=query)
            res.body = json.dumps([p.clean_dict() for p in db_res])


class CreateResource(BaseResource):
    """A basic resource for providing a model creation endpoint."""

    def on_post(self, req, res):
        """Create a new model and return the new model object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(jsn)
        with session() as db:
            db_res = self.store.new(db, actioning_user=user, **jsn)
            res.body = db_res.to_json()


class SingleResource(BaseResource):
    """A basic resource for retrieving a single model."""

    def on_get(self, req, res, uid):
        """Get a single model by uid.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-modelsuid
        """
        user = req.context['user']
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            if db_res is None:
                raise falcon.HTTPNotFound()
            res.body = db_res.to_json()


class UpdateResource(BaseResource):
    """A basic resource for updating a single model."""

    def on_put(self, req, res, uid):
        """Update the model indicated by uid.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelsuid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            db_res.name = jsn['name']
            self.store.update(db, actioning_user=user, model=db_res)

        res.body = json.dumps({
            'message': 'Successfully updated %s.' % self.model_name
        })


class DeleteResource(BaseResource):
    """A basic resource for deleting a single model."""

    def on_delete(self, req, res, uid):
        """Delete the model indicated by uid."""
        user = req.context['user']
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            print('deleting', db_res)
            self.store.delete(db, model=db_res, actioning_user=user)

        res.body = json.dumps({
            'message': 'Successfully deleted %s.' % self.model_name
        })


class BasicResource(SingleResource, UpdateResource, DeleteResource):
    """Handlers for the /api/v1/models/{uid} endpoint."""
    pass


class BasicMultiResource(SearchResource, CreateResource):
    """A basic resource class that can handle the modelNames endpoints."""
    pass
