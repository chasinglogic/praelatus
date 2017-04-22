"""Contains the API Resources for API V1."""

from praelatus.api.v1.users import UsersResource
from praelatus.api.v1.users import UserResource
from praelatus.api.v1.users import SessionResource
from praelatus.api.v1.tickets import TicketsResource


def add_v1_routes(app, prefix='/api/v1/'):
    """Add all of the v1 routes to the given app."""
    app.add_route(prefix+'users', UsersResource(SessionResource.create_session))
    app.add_route(prefix+'users/{username}', UserResource())
    app.add_route(prefix+'users/sessions', SessionResource())
    app.add_route(prefix+'tickets', TicketsResource())
