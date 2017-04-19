"""Contains the resources for the /api/v1/users endpoints."""

# flake8: noqa: D200

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

    def __init__(self, create_session):  # noqa: D400,D205
        """
        create_session should be a function which takes a user and a
        resp then creates a session in redis sending the session back
        to resp.

        Used for a user after signup.
        """
        self.create_session = create_session

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

    def on_post(self, req, resp):
        """Create a user."""
        user = json.load(req.stream)
        db_u = users.new(db(), **user)
        self.create_session(db_u, resp)


class UserResource():
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_get(self, req, resp, username):
        """Return single user by username or id."""
        user = req.context.get('user', {})
        db_res = users.get(db(), username=username, actioning_user=user)
        resp.body = db_res.to_json()

    def on_put(self, req, resp, username):
        """Update user."""
        jsn = json.load(req.stream)
        new_u = User.from_json(jsn)
        user = req.context.get('user', {})
        users.update(db(), actioning_user=user, user=new_u)
        resp.body = json.dumps({'message': 'Successfully updated user.'})

    def on_delete(self, req, resp, username):
        """Delete user."""
        sess = db()
        user = req.context.get('user', {})
        del_user = users.get(sess, username=username)
        users.delete(sess, actioning_user=user, user=del_user)
        resp.body = json.dumps({'message': 'Successfully deleted user.'})


class SessionResource():
    """Handlers for /api/v1/users/sessions endpoint."""

    def on_post(self, req, resp):
        """
        Create a new session AKA "log in".

        Accepts JSON of the form:

        ```json
        {
            "username": "testadmin",
            "password": "test"
        }
        ```

        Returns a session object as defined by schemas.session:

        ```json
        {
            "token": "some-auth-token",
            "user": {
                "full_name": "Test Testerson",
                "is_admin": true,
                "email": "test@example.com",
                "username": "testadmin",
                "id": 2,
                "is_active": true,
                "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
            }
        }
        ```
        """
        login = json.load(req.stream)
        user = users.get(db(), username=login['username'])
        if user is None:
            resp.body = json.dumps({
                'message': 'no user with that username exists.'
            })
            resp.status = falcon.HTTP_404
            return

        if not users.check_pw(user, login['password']):
            resp.body = json.dumps({'message': 'invalid password'})
            resp.status = falcon.HTTP_401
            return

        SessionResource.create_session(user, resp)

    @staticmethod
    def create_session(user, resp):
        """Create a session for user, set the resp body to the session."""
        # Check if the user is already logged in
        session_exists = sessions.get(user.username)

        if session_exists:
            token = session_exists
        else:
            token = str(sessions.gen_session_id())

        # Cookies take a datetime.datetime
        expires = datetime.now()+timedelta(hours=1)
        # Set takes a timedelta in seconds
        expires_seconds = expires - datetime.now()

        # Tie the token to the user
        sessions.set(token, user, expires=expires_seconds)
        # Tie the user to the token, used for checking if already
        # logged in
        sessions.set(user.username, token, expires=expires_seconds)

        # Set the session cookie on the response
        resp.set_cookie('PRAE_SESSION', token, expires=expires)

        resp.status = falcon.HTTP_200
        resp.body = json.dumps({
            'token': token,
            'user': user.clean_dict()
        })

    def on_delete(self, req, resp):
        """
        Invalidate the current user's session AKA "log out".
        
        No body is required for this endpoint.
        """
        sessions.delete(req.context.get('session_id'))
