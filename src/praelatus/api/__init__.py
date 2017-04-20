"""
Contains the app factory for the falcon.API.

This is where error handlers are registered and routes are added.
"""

import falcon
import json

from inspect import getdoc

from praelatus.api.v1 import add_v1_routes
from praelatus.api.errors import handle_error
from praelatus.api.middleware import AuthMiddleware
from praelatus.api.middleware import ContentTypeMiddleware


class RoutesResource():
    """Sends the full route listing as json."""

    def __init__(self, router):
        """Set self.routes, this should be app.router.roots."""
        self.router = router

    def parse_child(self, node):
        """Parse the compiled router node returning a useful json obj."""
        return {
            'url': node.uri_template,
            'methods': {
                'GET': getdoc(node.method_map['GET']),
                'PUT': getdoc(node.method_map['PUT']),
                'POST': getdoc(node.method_map['POST']),
                'DELETE': getdoc(node.method_map['DELETE'])
            }
        }

    def pull_children(self, router):
        """Traverse router getting routing info."""
        if hasattr(router, "children") and len(router.children) > 0:
            children = []
            for child in router.children:
                childs_children = self.pull_children(child)
                if childs_children:
                    children = children + childs_children
            if router.uri_template:
                return [self.parse_child(router)] + children
            return children
        return [self.parse_child(router)]

    def on_get(self, req, resp):
        """Send a json array of useful routing information."""
        routes = []
        for r in self.router:
            routes = routes + self.pull_children(r)
        resp.body = json.dumps(routes)


def create_app():
    """Factory method for our API."""
    app = falcon.API(middleware=[
        AuthMiddleware(),
        ContentTypeMiddleware()
    ])

    app.add_route('/api/routes', RoutesResource(app._router._roots))
    add_v1_routes(app)

    app.add_error_handler(Exception, handler=handle_error)
    return app
