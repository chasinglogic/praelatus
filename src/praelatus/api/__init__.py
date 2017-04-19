"""
Contains the app factory for the falcon.API.

This is where error handlers are registered and routes are added.
"""

import falcon
import json

from praelatus.api.v1 import add_v1_routes
from praelatus.models.permissions import PermissionError
from praelatus.api.errors import handle_permission_error
from praelatus.api.errors import handle_key_error
from praelatus.api.errors import handle_generic_error


class RoutesResource():
    """Sends the full route listing as json."""

    def __init__(self, routes):
        """Set self.routes, this should be app.router.roots."""
        self.routes = routes

    def on_get(self, req, resp):
        """Send self.routes as json."""
        resp.body = json.dumps(self.routes)
        resp.status = falcon.HTTP_200


def create_app():
    """Factory method for our API."""
    app = falcon.API()
    app.add_route('/api/routes', RoutesResource(app._router._roots))
    add_v1_routes(app)

    app.add_error_handler(Exception, handler=handle_generic_error)
    app.add_error_handler(PermissionError, handler=handle_permission_error)
    app.add_error_handler(KeyError, handler=handle_key_error)
    return app
