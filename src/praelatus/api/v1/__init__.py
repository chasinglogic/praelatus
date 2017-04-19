"""Contains the API Resources for API V1."""

from praelatus.api.v1.users import UsersResource
from praelatus.api.v1.users import UserResource


def add_v1_routes(app, prefix='/api/v1/'):
    """Add all of the v1 routes to the given app."""
    app.add_route(prefix+'users', UsersResource())
    app.add_route(prefix+'users/{username}', UserResource())
