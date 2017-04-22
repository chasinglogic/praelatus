"""Contains the resources for the /api/v1/users endpoints."""

# flake8: noqa: D200

import falcon
import json

from datetime import datetime
from datetime import timedelta

import praelatus.lib.users as users
import praelatus.lib.sessions as sessions

from praelatus.api.schemas import UserSchema
from praelatus.api.schemas import SignupSchema
from praelatus.models import User
from praelatus.lib import session as db


class UsersResource():
    """Handlers for the /api/v1/users endpoint."""

    def __init__(self, create_session):  # noqa: D400,D205
        """
        create_session should be a function which takes a user and a
        resp then creates a session in redis sending the session back
        to resp, it is called after on_post to create a session 
        for a user after signup.
        """
        self.create_session = create_session

    def on_get(self, req, resp):
        """
        Return all users for the instance.
        
        Accepts the query parameter filter which searches through
        users on the instance.
        
        Returns an array of user objects as defined by schemas.user
        
        ```json
        [
            {
                "full_name": "Test Testerson",
                "is_admin": true,
                "email": "test@example.com",
                "username": "testadmin",
                "id": 2,
                "is_active": true,
                "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
            },
            {
                "full_name": "Test Testerson II",
                "is_admin": false,
                "email": "test@example.com",
                "username": "testuser",
                "id": 3,
                "is_active": true,
                "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
            }
        ]
        ```
        """
        user = req.context.get('user', {})
        query = req.params.get('filter', '*')

        db_res = users.get(db(), filter=query,
                           actioning_user=user)
        usrs = []
        for u in db_res:
            usrs.append(u.clean_dict())

        resp.body = json.dumps(usrs)

    def on_post(self, req, resp):
        """
        Create a user and return the user object with the database
        information attached.
        
        Accepts JSON of the form:

        ```json
        {
            "username": "some_new_user",
            "password": "supersecure",
            "full_name": "New User",
            "email": "new@praelatus.io"
        }
        ```
        
        Returns a session object:
        
        ```json
        {
            "token": "1a2323f4-8eeb-4739-be43-1d5086ca5163",
            "user": {
                "id": 5,
                "full_name": "New User",
                "is_admin": false,
                "is_active": true,
                "email": "new@praelatus.io",
                "username": "some_new_user",
                "profile_pic": "https://gravatar.com/avatar/e688391c89d2551bf1f844249682ace4"
            }
        }
        ```
        """
        signup_req = json.loads(req.bounded_stream.read().decode('utf-8'))
        SignupSchema.validate(signup_req)
        db_u = users.new(db(), **signup_req)
        self.create_session(db_u, resp)


class UserResource():
    """Handlers for /api/v1/users/{username} endpoint."""

    def on_get(self, req, resp, username):
        """
        Return single user by username or id.

        Returns user object as defined by schemas.user:

        ```json
        {
            "full_name": "Test Testerson",
            "is_admin": true,
            "email": "test@example.com",
            "username": "testadmin",
            "id": 2,
            "is_active": true,
            "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
        }
        ```
        """
        user = req.context.get('user', {})
        db_res = users.get(db(), username=username, actioning_user=user)
        if db_res is None:
            resp.status = falcon.HTTP_404
            resp.body = json.dumps({
                'message': 'no user with that username exists'
            })
            return
        resp.body = db_res.to_json()

    def on_put(self, req, resp, username):
        """
        Update the user identified by username.

        Accepts a user object as defined by schemas.user:

        ```json
        {
            "full_name": "Test Testerson",
            "is_admin": true,
            "email": "test@example.com",
            "username": "testadmin",
            "id": 2,
            "is_active": true,
            "profile_pic": "https://gravatar.com/avatar/55502f40dc8b7c769880b10874abc9d0"
        }
        ```
        
        Returns a message indicating success or failure.
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        UserSchema.validate(jsn)
        sess = db()
        new_u = users.get(sess, username=username)
        if new_u is None:
            raise falcon.HTTPNotFound()
        new_u.username = jsn['username']
        new_u.email = jsn['email']
        new_u.profile_pic = jsn['profile_pic']
        new_u.full_name = jsn['full_name']
        new_u.is_active = jsn.get('is_active', True)
        new_u.is_admin = jsn.get('is_admin', False)
        users.update(sess, new_u, actioning_user=user)
        resp.body = json.dumps({'message': 'Successfully updated user.'})

    def on_delete(self, req, resp, username):
        """
        Delete the user identified by username.
        
        This request requires no body.
        
        Returns a message indicating success or failure.
        """
        user = req.context['user']
        sess = db()
        del_user = users.get(sess, username=username)
        if del_user is None:
            raise falcon.HTTPNotFound()
        users.delete(sess, del_user, actioning_user=user)
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

        Returns a session object:

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
        login = json.loads(req.bounded_stream.read().decode('utf-8'))
        user = users.get(db(), username=login['username'])
        if user is None:
            resp.body = json.dumps({
                'message': 'no user with that username exists'
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
        sessions.set(token, user.clean_dict(), expires=expires_seconds)
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
