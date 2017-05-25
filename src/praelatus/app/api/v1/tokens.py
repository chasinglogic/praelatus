"""Contains the resources for the /api/v1/users endpoints."""

import falcon
import json

import praelatus.lib.tokens as tokens

from praelatus.app.api.v1.base import BaseResource
from praelatus.lib import session


class TokensResource(BaseResource):
    """Handlers for /api/v1/tokens endpoint."""

    def on_post(self, req, res):
        """Create a new session AKA "log in".

        API Documentation:
        https://doc.praelatus.io/API/Reference/#post-tokens
        """
        login = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            user = self.store.get(db, username=login['username'])
        if user is None:
            res.body = json.dumps({
                'message': 'no user with that username exists'
            })
            res.status = falcon.HTTP_404
            return

        if not self.store.check_pw(user, login['password']):
            res.body = json.dumps({'message': 'invalid password'})
            res.status = falcon.HTTP_401
            return

        TokensResource.create_token(user, res)

    @staticmethod
    def create_token(user, res):
        """Create a session for user, set the res body to the session."""
        token = tokens.gen_session_id(user.jsonify())

        # Set the session cookie on the resonse
        res.set_cookie('PRAE_SESSION', token)

        res.status = falcon.HTTP_200
        res.body = json.dumps({
            'token': token,
            'user': user.jsonify()
        })
