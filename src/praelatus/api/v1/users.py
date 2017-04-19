"""Contains the resources for the /api/v1/users endpoints."""

import falcon
import json

import praelatus.lib.users as users

from praelatus.models import User
from praelatus.lib import session


class UsersResource():
    """Handlers for the /api/v1/users endpoint."""

    def on_get(self, req, resp):
        """Return all users."""
        user = req.context.get('user', {})
        query = req.params.get('filter', '*')

        db_res = users.get(session(), filter=query,
                           actioning_user=user)
        usrs = []
        for u in db_res:
            usrs.append(u.clean_dict())

        resp.body = json.dumps(usrs)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Create a user."""
        user = json.load(req.stream)
        db_u = users.new(session(), **user)
        resp.body = json.dumps(db_u)
        resp.status = falcon.HTTP_200


class UserResource():
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_get(self, req, resp, username):
        """Return single user by username or id."""
        user = req.context.get('user', {})
        db_res = users.get(session(), username=username,
                           actioning_user=user)
        resp.body = db_res.to_json()
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, username):
        """Update user."""
        jsn = json.load(req.stream)
        new_u = User.from_json(jsn)
        user = req.context.get('user', {})
        users.update(session(), actioning_user=user, user=new_u)
        resp.body = json.dumps({'message': 'Successfully updated user.'})
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, username):
        """Update user."""
        sess = session()
        user = req.context.get('user', {})
        del_user = users.get(sess, username=username)
        users.delete(sess, actioning_user=user, user=del_user)
        resp.body = json.dumps({'message': 'Successfully deleted user.'})
        resp.status = falcon.HTTP_200


# class SessionResource():
#     """Handlers for /api/v1/users/sessions endpoint."""

#     def on_get(self, req, resp):
