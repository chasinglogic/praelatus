"""Contains the API Resources for API V1."""

from flask import jsonify
from flask import request
from flask import abort
from flask import g

from praelatus.lib import connection
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

from praelatus.app.api.schemas import PermissionSchemeSchema
from praelatus.app.api.schemas import CommentSchema
from praelatus.app.api.schemas import TicketSchema
from praelatus.app.api.schemas import StatusSchema
from praelatus.app.api.schemas import UserSchema
from praelatus.app.api.schemas import FieldSchema
from praelatus.app.api.schemas import LabelSchema
from praelatus.app.api.schemas import TicketTypeSchema
from praelatus.app.api.schemas import ProjectSchema
from praelatus.app.api.schemas import WorkflowSchema
from praelatus.app.api.schemas import RoleSchema

from praelatus.app.api.v1.tickets import CommentResource
from praelatus.app.api.v1.tickets import CommentsResource
from praelatus.app.api.v1.tickets import TicketResource
from praelatus.app.api.v1.tickets import TicketsResource
from praelatus.app.api.v1.tokens import TokensResource
from praelatus.app.api.v1.base import BasicMultiResource
from praelatus.app.api.v1.base import BasicResource
from praelatus.app.api.v1.base import BaseResource


class ProjectResource(BasicResource):
    """Handlers for the /api/v1/projects/{uid} endpoint."""

    def delete(self, uid):
        """Delete the project indicated by uid."""

        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            self.store.delete(db, model=db_res,
                              project=db_res, actioning_user=g.user)
        return jsonify({
            'message': 'Successfully deleted %s.' % self.model_name
        })

    def put(self, uid):
        """Update the project indicated by uid."""
        jsn = request.get_json()
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            db_res.name = jsn['name']
            db_res.key = jsn['key']
            db_res.homepage = jsn.get('homepage', db_res.homepage)
            db_res.icurl = jsn.get('icurl', db_res.icurl)
            db_res.repo = jsn.get('repo', db_res.repo)
            scheme = jsn.get('permissischeme')
            if scheme is not None:
                db_res.permissischeme_id = scheme['id']

            lead = jsn.get('lead')
            if lead is not None:
                db_res.lead_id = lead['id']

            self.store.update(db, model=db_res,
                              project=db_res, actioning_user=g.user)
        return jsonify({
            'message': 'Successfully updated %s.' % self.model_name
        })


class UsersResource(BasicMultiResource):
    """Handlers for the /api/v1/users endpoint."""

    def __init__(self, store, schema, create_token):  # noqa: D400,D205
        """create_token should be a function which takes a user and a res
        then creates a token for that user and sends it to res, it is
        called after post to create a token for a user after
        signup.
        """
        super(UsersResource, self).__init__(store, schema)
        self.create_token = create_token

    def post(self):
        """Create a user then return that user with an auth token.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-users
        """
        signup_req = request.get_json()
        self.schema.validate(signup_req)
        with connection() as db:
            db_u = self.store.new(db, **signup_req)
            return self.create_token(db_u)


class UserResource(BasicResource):
    """Handlers for /api/v1/users/{username} endpoint."""

    def put(self, uid):
        """Update the user identified by username.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-usersusername
        """
        jsn = request.get_json()
        self.schema.validate(jsn)
        with connection() as db:
            new_u = self.store.get(db, uid=uid)
            if new_u is None:
                abort(404)
            new_u.username = jsn['username']
            new_u.email = jsn['email']
            new_u.profile_pic = jsn['profile_pic']
            new_u.full_name = jsn['full_name']
            new_u.is_active = jsn.get('is_active', True)
            new_u.is_admin = jsn.get('is_admin', False)
            self.store.update(db, model=new_u, actioning_user=g.user)
        return jsonify({'message': 'Successfully updated user.'})


class AssignedResource(BaseResource):
    """Handlers for the /api/v1/users/{username}/assigned endpoint."""

    def __init__(self, store, schema, user_store):
        """Add user_store to BaseResource."""
        super(AssignedResource, self).__init__(store, schema)
        self.user_store = user_store

    def get(self, uid):
        """"Get all reported tickets by username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernamereported
        """
        with connection() as db:
            assignee = self.user_store.get(db, uid=uid)
            ticks = self.store.search(db, actioning_user=g.user,
                                      assignee=assignee.jsonify())
            return jsonify([t.jsonify() for t in ticks])


class ReportedResource(BaseResource):
    """Handlers for the /api/v1/users/{uid}/reported endpoint."""

    def __init__(self, store, schema, user_store):
        """Add user_store to BaseResource."""
        super(ReportedResource, self).__init__(store, schema)
        self.user_store = user_store

    def get(self, uid):
        """"Get all reported tickets by username.

        API Documentation:
        https://doc.praelatus.io/API/Reference/#get-usersusernamereported
        """
        with connection() as db:
            reporter = self.user_store.get(db, uid=uid)
            ticks = self.store.search(db, actioning_user=g.user,
                                      reporter=reporter.jsonify())
            return jsonify([t.jsonify() for t in ticks])


class ProjectTicketsResource(BasicResource):
    """Handlers for the /api/v1/projects/{key}/tickets endpoint."""

    def get(self, uid):
        """Get all tickets for project with key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-projectskeytickets
        """
        with connection() as db:
            db_res = TicketStore.search(db, actioning_user=g.user,
                                        project_key=uid)
            return jsonify([t.jsonify() for t in db_res])


class WorkflowResource(BasicResource):
    """Overrides put method from BasicResource."""

    def put(self, uid):
        """Update the workflow indicated by id."""
        jsn = request.get_json()
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            updated = self.store.update_from_json(db, db_res, jsn,
                                                  actioning_user=g.user)
            self.store.update(db, actioning_user=g.user, model=updated)

        return jsonify({'message': 'Successfully update workflow.'})


class FieldResource(BasicResource):
    """Overrides put method from BasicResource."""

    def put(self, uid):
        """Update the field indicated by id."""
        jsn = request.get_json()
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user, uid=uid)
            db_res.name = jsn['name']
            db_res.data_type = jsn['data_type']
            opts = jsn.get('options')
            if db_res.data_type == 'OPT' and opts:
                for o in opts:
                    db_res.options.append(FieldOption(name=o))
            self.store.update(db, actioning_user=g.user, model=db_res)

        return jsonify({'message': 'Successfully update field.'})


def add_v1_routes(blueprint, prefix='/api/v1/'):
    """Add all of the v1 routes to the given blueprint."""
    # Users
    blueprint.\
        add_url_rule(prefix + 'users',
                     view_func=UsersResource.
                     as_view(
                         prefix + 'users',
                         UserStore,
                         UserSchema,
                         TokensResource.create_token))
    blueprint.\
        add_url_rule(prefix + 'users/<uid>',
                     view_func=UserResource.
                     as_view(prefix + 'user',
                             UserStore,
                             UserSchema))
    blueprint.\
        add_url_rule(prefix + 'users/<uid>/reported',
                     view_func=ReportedResource.
                     as_view(
                         prefix + 'reported',
                         TicketStore,
                         None,
                         UserStore))
    blueprint.\
        add_url_rule(prefix + 'users/<uid>/assigned',
                     view_func=AssignedResource.
                     as_view(
                         prefix + 'assigned',
                         TicketStore,
                         None,
                         UserStore))

    # Tokens
    blueprint.\
        add_url_rule(prefix + 'tokens',
                     view_func=TokensResource.
                     as_view(
                         prefix + 'tokens',
                         UserStore,
                         None))
    # Tickets
    blueprint.\
        add_url_rule(prefix + 'tickets',
                     view_func=TicketsResource.
                     as_view(prefix + 'tickets',
                             TicketStore,
                             TicketSchema))
    blueprint.\
        add_url_rule(prefix + 'tickets/<ticket_key>',
                     view_func=TicketResource.
                     as_view(prefix + 'ticket',
                             TicketStore,
                             TicketSchema))

    # Comments
    blueprint.\
        add_url_rule(prefix + 'tickets/<ticket_key>/comments',
                     view_func=CommentsResource.
                     as_view(
                         prefix + 'comments',
                         CommentStore,
                         CommentSchema,
                         TicketStore))
    blueprint.\
        add_url_rule(prefix + 'tickets/<ticket_key>/comments/<id>',
                     view_func=CommentResource.
                     as_view(
                         prefix + 'comment',
                         CommentStore,
                         CommentSchema,
                         TicketStore))

    # Projects
    blueprint.\
        add_url_rule(prefix + 'projects',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'projects',
                             ProjectStore,
                             ProjectSchema))
    blueprint.\
        add_url_rule(prefix + 'projects/<uid>',
                     view_func=ProjectResource.
                     as_view(prefix + 'project',
                             ProjectStore,
                             ProjectSchema))
    blueprint.\
        add_url_rule(prefix + 'projects/<uid>/tickets',
                     view_func=ProjectTicketsResource.
                     as_view(
                         prefix + 'project_tickets',
                         TicketStore,
                         None))

    # TicketTypes
    blueprint.\
        add_url_rule(prefix + 'ticketTypes',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'types',
                             TicketTypeStore,
                             TicketTypeSchema))
    blueprint.\
        add_url_rule(prefix + 'ticketTypes/<uid>',
                     view_func=BasicResource.
                     as_view(prefix + 'type',
                             TicketTypeStore,
                             TicketTypeSchema))

    # Statuses
    blueprint.\
        add_url_rule(prefix + 'statuses',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'statuses',
                             StatusStore,
                             StatusSchema))
    blueprint.\
        add_url_rule(prefix + 'statuses/<uid>',
                     view_func=BasicResource.
                     as_view(prefix + 'status',
                             StatusStore,
                             StatusSchema))

    # Labels
    blueprint.\
        add_url_rule(prefix + 'labels',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'labels',
                             LabelStore,
                             LabelSchema))
    blueprint.\
        add_url_rule(prefix + 'labels/<uid>',
                     view_func=BasicResource.
                     as_view(prefix + 'label',
                             LabelStore,
                             LabelSchema))

    # Fields
    blueprint.\
        add_url_rule(prefix + 'fields',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'fields',
                             FieldStore,
                             FieldSchema))
    blueprint.\
        add_url_rule(prefix + 'fields/<uid>',
                     view_func=FieldResource.
                     as_view(prefix + 'field',
                             FieldStore,
                             FieldSchema))

    # Workflows
    blueprint.\
        add_url_rule(prefix + 'workflows',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'workflows',
                             WorkflowStore,
                             WorkflowSchema))

    blueprint.\
        add_url_rule(prefix + 'workflows/<uid>',
                     view_func=WorkflowResource.
                     as_view(prefix + 'workflow',
                             WorkflowStore,
                             WorkflowSchema))

    # Roles
    blueprint.\
        add_url_rule(prefix + 'roles',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'roles',
                             RoleStore,
                             RoleSchema))
    blueprint.\
        add_url_rule(prefix + 'roles/<uid>',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'role',
                             RoleStore,
                             RoleSchema))

    # Permission Schemes
    blueprint.\
        add_url_rule(prefix + 'permissionSchemes',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'schemes',
                             PermissionSchemeStore,
                             PermissionSchemeSchema))
    blueprint.\
        add_url_rule(prefix + 'permissionSchemes/<uid>',
                     view_func=BasicMultiResource.
                     as_view(prefix + 'scheme',
                             PermissionSchemeStore,
                             PermissionSchemeSchema))
