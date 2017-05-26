"""Contains resources for interacting with self.store."""

from flask.views import MethodView
from flask import jsonify
from flask import request
from flask import g

from praelatus.lib import connection


class BaseResource(MethodView):
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

    def get(self):
        """Get all of the correct model the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available self.store.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        query = request.args.get('filter', '*')
        with connection() as db:
            db_res = self.store.search(db, actioning_user=g.user, search=query)
            return jsonify([p.jsonify() for p in db_res])


class CreateResource(BaseResource):
    """A basic resource for providing a model creation endpoint."""

    def post(self):
        """Create a new model and return the new model object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        jsn = request.get_json()
        self.schema.validate(jsn)
        with connection() as db:
            db_res = self.store.new(db, actioning_user=g.user, **jsn)
            return jsonify(db_res.jsonify())


class SingleResource(BaseResource):
    """A basic resource for retrieving a single model."""

    def get(self, uid):
        """Get a single model by uid.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-modelsuid
        """
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            if db_res is None:
                raise falcon.HTTPNotFound()
            return jsonify(db_res.jsonify())


class UpdateResource(BaseResource):
    """A basic resource for updating a single model."""

    def put(self, uid):
        """Update the model indicated by uid.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelsuid
        """
        jsn = request.get_json()
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            db_res.name = jsn['name']
            self.store.update(db, actioning_user=g.user, model=db_res)

        return jsonify({
            'message': 'Successfully updated %s.' % self.model_name
        })


class DeleteResource(BaseResource):
    """A basic resource for deleting a single model."""

    def delete(self, uid):
        """Delete the model indicated by uid."""
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            print('deleting', db_res)
            self.store.delete(db, model=db_res, actioning_user=g.user)

        return jsonify({
            'message': 'Successfully deleted %s.' % self.model_name
        })


class BasicResource(SingleResource, UpdateResource, DeleteResource):
    """Handlers for the /api/v1/models/{uid} endpoint."""
    pass


class BasicMultiResource(SearchResource, CreateResource):
    """A basic resource class that can handle the modelNames endpoints."""
    pass
