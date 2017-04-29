"""Contains the API Resources for API V1."""

from praelatus.api.v1.users import UsersResource
from praelatus.api.v1.users import UserResource
from praelatus.api.v1.users import TokensResource
from praelatus.api.v1.users import ReportedResource
from praelatus.api.v1.users import AssignedResource
from praelatus.api.v1.tickets import TicketsResource
from praelatus.api.v1.tickets import TicketResource
from praelatus.api.v1.tickets import CommentsResource
from praelatus.api.v1.tickets import CommentResource
from praelatus.api.v1.projects import ProjectsResource
from praelatus.api.v1.projects import ProjectTicketsResource
from praelatus.api.v1.projects import ProjectResource
from praelatus.api.v1.ticket_types import TicketTypesResource
from praelatus.api.v1.ticket_types import TicketTypeResource
from praelatus.api.v1.statuses import StatusesResource
from praelatus.api.v1.statuses import StatusResource
from praelatus.api.v1.fields import FieldsResource
from praelatus.api.v1.fields import FieldResource
from praelatus.api.v1.labels import LabelsResource
from praelatus.api.v1.labels import LabelResource
from praelatus.api.v1.workflows import WorkflowsResource
from praelatus.api.v1.workflows import WorkflowResource


def add_v1_routes(app, prefix='/api/v1/'):
    """Add all of the v1 routes to the given app."""
    # Users
    app.add_route(prefix + 'users',
                  UsersResource(TokensResource.create_token))
    app.add_route(prefix + 'users/{username}', UserResource())
    app.add_route(prefix + 'users/{username}/reported', ReportedResource())
    app.add_route(prefix + 'users/{username}/assigned', AssignedResource())

    # Tokens
    app.add_route(prefix + 'tokens', TokensResource())

    # Tickets
    app.add_route(prefix + 'tickets', TicketsResource())
    app.add_route(prefix + 'tickets/{ticket_key}', TicketResource())

    # Comments
    app.add_route(prefix + 'tickets/{ticket_key}/comments',
                  CommentsResource())
    app.add_route(prefix + 'tickets/{ticket_key}/comments/{id}',
                  CommentResource())

    # Projects
    app.add_route(prefix + 'projects', ProjectsResource())
    app.add_route(prefix + 'projects/{key}', ProjectResource())
    app.add_route(prefix + 'projects/{key}/tickets', ProjectTicketsResource())

    # TicketTypes
    app.add_route(prefix + 'ticketTypes', TicketTypesResource())
    app.add_route(prefix + 'ticketTypes/{id}', TicketTypeResource())

    # Statuses
    app.add_route(prefix + 'statuses', StatusesResource())
    app.add_route(prefix + 'statuses/{id}', StatusResource())

    # Labels
    app.add_route(prefix + 'labels', LabelsResource())
    app.add_route(prefix + 'labels/{id}', LabelResource())

    # Fields
    app.add_route(prefix + 'fields', FieldsResource())
    app.add_route(prefix + 'fields/{id}', FieldResource())

    # Workflows
    app.add_route(prefix + 'workflows', WorkflowsResource())
    app.add_route(prefix + 'workflows/{id}', WorkflowResource())
