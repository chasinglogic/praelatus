"""Contains the API Resources for API V1."""

import json
import falcon

from praelatus.lib import session
from praelatus.models.fields import FieldOption

from praelatus.store import WorkflowStore
from praelatus.store import TicketStore
from praelatus.store import ProjectStore
from praelatus.store import LabelStore
from praelatus.store import FieldStore
from praelatus.store import PermissionSchemeStore
from praelatus.store import RoleStore
from praelatus.store import TicketTypeStore
from praelatus.store import StatusStore
from praelatus.store import CommentStore
from praelatus.store import UserStore

from praelatus.api.schemas import PermissionSchemeSchema
from praelatus.api.schemas import CommentSchema
from praelatus.api.schemas import TicketSchema
from praelatus.api.schemas import StatusSchema
from praelatus.api.schemas import UserSchema
from praelatus.api.schemas import FieldSchema
from praelatus.api.schemas import LabelSchema
from praelatus.api.schemas import TicketTypeSchema
from praelatus.api.schemas import ProjectSchema
from praelatus.api.schemas import WorkflowSchema
from praelatus.api.schemas import RoleSchema

from praelatus.api.v1.tickets import CommentResource
from praelatus.api.v1.tickets import CommentsResource
from praelatus.api.v1.tickets import TicketResource
from praelatus.api.v1.tickets import TicketsResource
from praelatus.api.v1.tokens import TokensResource
from praelatus.api.v1.base import BasicMultiResource
from praelatus.api.v1.base import BasicResource
from praelatus.api.v1.base import BaseResource


class ProjectResource(BasicResource):
    """Handlers for the /api/v1/projects/{uid} endpoint."""

    def on_delete(self, req, res, uid):
        """Delete the project indicated by uid."""
        user = req.context['user']
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            self.store.delete(db, model=db_res,
                              project=db_res, actioning_user=user)
        res.body = json.dumps({
            'message': 'Successfully deleted %s.' % self.model_name
        })

    def on_put(self, req, res, uid):
        """Update the project indicated by uid."""
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            db_res.name = jsn['name']
            db_res.key = jsn['key']
            db_res.homepage = jsn.get('homepage', db_res.homepage)
            db_res.icon_url = jsn.get('icon_url', db_res.icon_url)
            db_res.repo = jsn.get('repo', db_res.repo)
            scheme = jsn.get('permission_scheme')
            if scheme is not None:
                db_res.permission_scheme_id = scheme['id']

            lead = jsn.get('lead')
            if lead is not None:
                db_res.lead_id = lead['id']

            self.store.update(db, model=db_res,
                              project=db_res, actioning_user=user)
        res.body = json.dumps({
            'message': 'Successfully updated %s.' % self.model_name
        })


class UsersResource(BasicMultiResource):
    """Handlers for the /api/v1/users endpoint."""

    def __init__(self, store, schema, create_token):  # noqa: D400,D205
        """create_token should be a function which takes a user and a res
        then creates a token for that user and sends it to res, it is
        called after on_post to create a token for a user after
        signup.
        """
        super(UsersResource, self).__init__(store, schema)
        self.create_token = create_token

    def on_post(self, req, res):
        """Create a user then return that user with an auth token.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-users
        """
        signup_req = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(signup_req)
        with session() as db:
            db_u = self.store.new(db, **signup_req)
            self.create_token(db_u, res)


class UserResource(BasicResource):
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_put(self, req, res, uid):
        """Update the user identified by username.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-usersusername
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(jsn)
        with session() as db:
            new_u = self.store.get(db, uid=uid)
            if new_u is None:
                raise falcon.HTTPNotFound()
            new_u.username = jsn['username']
            new_u.email = jsn['email']
            new_u.profile_pic = jsn['profile_pic']
            new_u.full_name = jsn['full_name']
            new_u.is_active = jsn.get('is_active', True)
            new_u.is_admin = jsn.get('is_admin', False)
            self.store.update(db, model=new_u, actioning_user=user)
        res.body = json.dumps({'message': 'Successfully updated user.'})


class AssignedResource(BaseResource):
    """Handlers for the /api/v1/users/{username}/assigned endpoint."""

    def __init__(self, store, schema, user_store):
        """Add user_store to BaseResource."""
        super(AssignedResource, self).__init__(store, schema)
        self.user_store = user_store

    def on_get(self, req, res, uid):
        """"Get all reported tickets by username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernamereported
        """
        user = req.context['user']
        with session() as db:
            assignee = self.user_store.get(db, uid=uid)
            ticks = self.store.search(db, actioning_user=user,
                                      assignee=assignee.clean_dict())
            res.body = json.dumps([t.clean_dict() for t in ticks])


class ReportedResource(BaseResource):
    """Handlers for the /api/v1/users/{uid}/reported endpoint."""

    def __init__(self, store, schema, user_store):
        """Add user_store to BaseResource."""
        super(ReportedResource, self).__init__(store, schema)
        self.user_store = user_store

    def on_get(self, req, res, uid):
        """"Get all reported tickets by username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernamereported
        """
        user = req.context['user']
        with session() as db:
            reporter = self.user_store.get(db, uid=uid)
            ticks = self.store.search(db, actioning_user=user,
                                      reporter=reporter.clean_dict())
            res.body = json.dumps([t.clean_dict() for t in ticks])


class ProjectTicketsResource(BaseResource):
    """Handlers for the /api/v1/projects/{key}/tickets."""

    def on_get(self, req, res, uid):
        """Get all tickets for project with key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-projectskeytickets
        """
        user = req.context['user']
        with session() as db:
            db_res = self.store.search(db, actioning_user=user,
                                       project_key=uid)
            res.body = json.dumps([t.clean_dict() for t in db_res])


class WorkflowResource(BasicResource):
    """Overrides on_put method from BasicResource."""

    def on_put(self, req, resp, uid):
        """Update the workflow indicated by id."""
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            updated = self.store.update_from_json(db, db_res, jsn,
                                                  actioning_user=user)
            self.store.update(db, actioning_user=user, model=updated)

        resp.body = json.dumps({'message': 'Successfully update workflow.'})


class FieldResource(BasicResource):
    """Overrides on_put method from BasicResource."""

    def on_put(self, req, resp, uid):
        """Update the field indicated by id."""
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.store.get(db, actioning_user=user, uid=uid)
            db_res.name = jsn['name']
            db_res.data_type = jsn['data_type']
            opts = jsn.get('options')
            if db_res.data_type == 'OPT' and opts:
                for o in opts:
                    db_res.options.append(FieldOption(name=o))
            self.store.update(db, actioning_user=user, model=db_res)

        resp.body = json.dumps({'message': 'Successfully update field.'})


def add_v1_routes(app, prefix='/api/v1/'):
    """Add all of the v1 routes to the given app."""
    # Users
    app.add_route(prefix + 'users',
                  UsersResource(UserStore, UserSchema,
                                TokensResource.create_token))
    app.add_route(prefix + 'users/{uid}',
                  UserResource(UserStore, UserSchema))

    app.add_route(prefix + 'users/{uid}/reported',
                  ReportedResource(TicketStore, None, UserStore))
    app.add_route(prefix + 'users/{uid}/assigned',
                  AssignedResource(TicketStore, None, UserStore))

    # Tokens
    app.add_route(prefix + 'tokens',
                  TokensResource(UserStore, None))

    # Tickets
    app.add_route(prefix + 'tickets',
                  TicketsResource(TicketStore, TicketSchema))
    app.add_route(prefix + 'tickets/{ticket_key}',
                  TicketResource(TicketStore, TicketSchema))

    # Comments
    app.add_route(prefix + 'tickets/{ticket_key}/comments',
                  CommentsResource(CommentStore, CommentSchema, TicketStore))
    app.add_route(prefix + 'tickets/{ticket_key}/comments/{id}',
                  CommentResource(CommentStore, CommentSchema, TicketStore))

    # Projects
    app.add_route(prefix + 'projects',
                  BasicMultiResource(ProjectStore, ProjectSchema))
    app.add_route(prefix + 'projects/{uid}',
                  ProjectResource(ProjectStore, ProjectSchema))
    app.add_route(prefix + 'projects/{uid}/tickets',
                  ProjectTicketsResource(TicketStore, None))

    # TicketTypes
    app.add_route(prefix + 'ticketTypes',
                  BasicMultiResource(TicketTypeStore, TicketTypeSchema))
    app.add_route(prefix + 'ticketTypes/{uid}',
                  BasicResource(TicketTypeStore, TicketTypeSchema))

    # Statuses
    app.add_route(prefix + 'statuses',
                  BasicMultiResource(StatusStore, StatusSchema))
    app.add_route(prefix + 'statuses/{uid}',
                  BasicResource(StatusStore, StatusSchema))

    # Labels
    app.add_route(prefix + 'labels',
                  BasicMultiResource(LabelStore, LabelSchema))
    app.add_route(prefix + 'labels/{uid}',
                  BasicResource(LabelStore, LabelSchema))

    # Fields
    app.add_route(prefix + 'fields',
                  BasicMultiResource(FieldStore, FieldSchema))
    app.add_route(prefix + 'fields/{uid}',
                  FieldResource(FieldStore, FieldSchema))

    # Workflows
    app.add_route(prefix + 'workflows',
                  BasicMultiResource(WorkflowStore, WorkflowSchema))
    app.add_route(prefix + 'workflows/{uid}',
                  WorkflowResource(WorkflowStore, WorkflowSchema))

    # Roles
    app.add_route(prefix + 'roles',
                  BasicMultiResource(RoleStore, RoleSchema))
    app.add_route(prefix + 'roles/{uid}',
                  BasicMultiResource(RoleStore, RoleSchema))

    # Permission Schemes
    app.add_route(prefix + 'permissionSchemes',
                  BasicMultiResource(PermissionSchemeStore, PermissionSchemeSchema))
    app.add_route(prefix + 'permissionSchemes/{uid}',
                  BasicMultiResource(PermissionSchemeStore, PermissionSchemeSchema))
