"""Contains resources for interacting with self.store."""

from werkzeug.exceptions import NotFound
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


class BasicResource(BaseResource):
    """Handlers for the /api/v1/models/{uid} endpoint."""

    def get(self, uid):
        """Get a single model by uid.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-modelsuid
        """
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            if db_res is None:
                raise NotFound()
            return jsonify(db_res.jsonify())

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

    def delete(self, uid):
        """Delete the model indicated by uid."""
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            print('deleting', db_res)
            self.store.delete(db, model=db_res, actioning_user=g.user)

        return jsonify({
            'message': 'Successfully deleted %s.' % self.model_name
        })


class BasicMultiResource(BaseResource):
    """A basic resource class that can handle the modelNames endpoints."""

    def get(self):
        """Get all of the correct model the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available self.store.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        query = request.args.get('filter', '*')
        start = int(request.args.get('start', '0'))
        limit = int(request.args.get('limit', '50'))
        with connection() as db:
            db_res = self.store.search(db, actioning_user=g.user, search=query,
                                       limit=limit, offset=start)
            return jsonify({
                'start': start,
                'results': [p.jsonify() for p in db_res]
            })

    def post(self):
        """Create a new model and return the new model object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-models
        """
        jsn = request.get_json()
        print('jsn', jsn)
        self.schema.validate(jsn)
        with connection() as db:
            db_res = self.store.new(db, actioning_user=g.user, **jsn)
            return jsonify(db_res.jsonify())
