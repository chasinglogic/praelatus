"""Contains the API Resources for API V1."""

import json

import praelatus.lib.ticket_types as ticket_types
import praelatus.lib.fields as fields
import praelatus.lib.projects
import praelatus.lib.statuses as statuses
import praelatus.lib.labels as labels
import praelatus.lib.workflows as workflows

from praelatus.lib import session
from praelatus.models.fields import FieldOption
from praelatus.api.schemas import LabelSchema
from praelatus.api.schemas import WorkflowSchema
from praelatus.api.schemas import StatusSchema
from praelatus.api.schemas import ProjectSchema
from praelatus.api.schemas import TicketTypeSchema
from praelatus.api.schemas import FieldSchema
from praelatus.api.v1.users import UsersResource
from praelatus.api.v1.users import UserResource
from praelatus.api.v1.users import TokensResource
from praelatus.api.v1.users import ReportedResource
from praelatus.api.v1.users import AssignedResource
from praelatus.api.v1.tickets import TicketsResource
from praelatus.api.v1.tickets import TicketResource
from praelatus.api.v1.tickets import CommentsResource
from praelatus.api.v1.tickets import CommentResource
from praelatus.api.v1.projects import ProjectTicketsResource
from praelatus.api.v1.projects import ProjectResource
from praelatus.api.v1.base import BasicMultiResource
from praelatus.api.v1.base import BasicResource


class WorkflowResource(BasicResource):
    """Overrides on_put method from BasicResource."""

    def on_put(self, req, resp, id):
        """Update the workflow indicated by id."""
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, id=id)
            updated = self.lib.update_from_json(db, db_res, jsn,
                                                actioning_user=user)
            self.lib.update(db, actioning_user=user, workflow=updated)

        resp.body = json.dumps({'message': 'Successfully update workflow.'})


class FieldResource(BasicResource):
    """Overrides on_put method from BasicResource."""

    def on_put(self, req, resp, id):
        """Update the field indicated by id."""
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, id=id)
            db_res.name = jsn['name']
            db_res.data_type = jsn['data_type']
            opts = jsn.get('options')
            if db_res.data_type == 'OPT' and opts:
                for o in opts:
                    db_res.options.append(FieldOption(name=o))
            self.lib.update(db, actioning_user=user, field=db_res)

        resp.body = json.dumps({'message': 'Successfully update field.'})


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
    app.add_route(prefix + 'projects',
                  # For some reason if we just use projects it
                  # attempts to use the api submodule so use full name
                  # here
                  BasicMultiResource(praelatus.lib.projects, ProjectSchema))
    app.add_route(prefix + 'projects/{key}',
                  ProjectResource())
    app.add_route(prefix + 'projects/{key}/tickets', ProjectTicketsResource())

    # TicketTypes
    app.add_route(prefix + 'ticketTypes',
                  BasicMultiResource(ticket_types, TicketTypeSchema))
    app.add_route(prefix + 'ticketTypes/{id}',
                  BasicResource(ticket_types, TicketTypeSchema))

    # Statuses
    app.add_route(prefix + 'statuses',
                  BasicMultiResource(statuses, StatusSchema,
                                     model_name='status'))
    app.add_route(prefix + 'statuses/{id}',
                  BasicResource(statuses, StatusSchema,
                                model_name='status'))

    # Labels
    app.add_route(prefix + 'labels',
                  BasicMultiResource(labels, LabelSchema))
    app.add_route(prefix + 'labels/{id}',
                  BasicResource(labels, LabelSchema))

    # Fields
    app.add_route(prefix + 'fields',
                  BasicMultiResource(fields, FieldSchema))
    app.add_route(prefix + 'fields/{id}',
                  FieldResource(fields, FieldSchema))

    # Workflows
    app.add_route(prefix + 'workflows',
                  BasicMultiResource(workflows, WorkflowSchema))
    app.add_route(prefix + 'workflows/{id}',
                  WorkflowResource(workflows, WorkflowSchema))
