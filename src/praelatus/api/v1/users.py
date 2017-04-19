"""Contains the resources for the /api/v1/users endpoints."""

import falcon
import json

from datetime import datetime
from datetime import timedelta

import praelatus.lib.users as users
import praelatus.lib.sessions as sessions

from praelatus.models import User
from praelatus.lib import session as db


class UsersResource():
    """Handlers for the /api/v1/users endpoint."""

    def on_get(self, req, resp):
        """Return all users."""
        user = req.context.get('user', {})
        query = req.params.get('filter', '*')

        db_res = users.get(db(), filter=query,
                           actioning_user=user)
        usrs = []
        for u in db_res:
            usrs.append(u.clean_dict())

        resp.body = json.dumps(usrs)
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        """Create a user."""
        user = json.load(req.stream)
        db_u = users.new(db(), **user)
        resp.body = json.dumps(db_u)
        resp.status = falcon.HTTP_200


class UserResource():
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_get(self, req, resp, username):
        """Return single user by username or id."""
        user = req.context.get('user', {})
        db_res = users.get(db(), username=username,
                           actioning_user=user)
        resp.body = db_res.to_json()
        resp.status = falcon.HTTP_200

    def on_put(self, req, resp, username):
        """Update user."""
        jsn = json.load(req.stream)
        new_u = User.from_json(jsn)
        user = req.context.get('user', {})
        users.update(db(), actioning_user=user, user=new_u)
        resp.body = json.dumps({'message': 'Successfully updated user.'})
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, username):
        """Update user."""
        sess = db()
        user = req.context.get('user', {})
        del_user = users.get(sess, username=username)
        users.delete(sess, actioning_user=user, user=del_user)
        resp.body = json.dumps({'message': 'Successfully deleted user.'})
        resp.status = falcon.HTTP_200


class SessionResource():
    """Handlers for /api/v1/users/sessions endpoint."""

    def on_post(self, req, resp):
        """Used for creating a new session or "logging in"."""
        login = json.load(req.stream)
        user = users.get(db(), username=login['username'])
        if user is None:
            resp.body = json.dumps({
                'message': 'no user with that username exists.'
            })
            resp.status = falcon.HTTP_404
        elif users.check_pw(user, login['password']):
            sess_id = sessions.gen_session_id()
            sessions.set(sess_id, user)
            resp.set_cookie('PRAE_SESSION', sess_id,
                            expires=datetime.now()+timedelta(hours=1))
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({'message': 'invalid password'})
            resp.status = falcon.HTTP_401

    def on_delete(self, req, resp):
        """Used for invalidating sessions or "logging out"."""
        sessions.delete(req.context.get('session_id'))
