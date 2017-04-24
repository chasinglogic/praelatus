"""Contains the API Resources for API V1."""

from praelatus.api.v1.users import UsersResource
from praelatus.api.v1.users import UserResource
from praelatus.api.v1.users import TokensResource
from praelatus.api.v1.tickets import TicketsResource
from praelatus.api.v1.tickets import TicketResource


def add_v1_routes(app, prefix='/api/v1/'):
    """Add all of the v1 routes to the given app."""
    app.add_route(prefix + 'users',
                  UsersResource(TokensResource.create_token))
    app.add_route(prefix + 'users/{username}', UserResource())
    app.add_route(prefix + 'tokens', TokensResource())
    app.add_route(prefix + 'tickets', TicketsResource())
    app.add_route(prefix + 'tickets/{key}', TicketResource())
