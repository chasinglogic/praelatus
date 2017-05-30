"""Contains the resources for the /api/v1/users endpoints."""

from flask import jsonify
from flask import request

import praelatus.lib.tokens as tokens

from praelatus.app.api.v1.base import BaseResource
from praelatus.lib import connection


class TokensResource(BaseResource):
    """Handlers for /api/v1/tokens endpoint."""

    def post(self):
        """Create a new connection AKA "log in".

        API Documentation:
        https://doc.praelatus.io/API/Reference/#post-tokens
        """
        login = request.get_json()
        with connection() as db:
            user = self.store.get(db, username=login['username'])
            if user is None:
                res = jsonify({
                    'message': 'no user with that username exists'
                })
                res.status_code = 404
                return res

            if not self.store.check_pw(user, login['password']):
                res = jsonify({'message': 'invalid password'})
                res.status_code = 401
                return res

            return TokensResource.create_token(user)

    @staticmethod
    def create_token(user):
        """Create a connection for user, set the res body to the connection."""
        token = tokens.gen_session_id(user.jsonify())
        return jsonify({
            'token': token,
            'user': user.jsonify()
        })
