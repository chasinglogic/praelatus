"""Blueprint for the api endpoints."""

import json
import itsdangerous
import praelatus.lib.tokens as tokens

from flask import Blueprint
from flask import request
from flask import g

from praelatus.app.api.v1 import add_v1_routes

# Fix python 3.4 to 3.5 compatibility
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

api = Blueprint('api', __name__)

# Register /api/v1/ routes.
add_v1_routes(api)

# Make v1 the latest version.
add_v1_routes(api, prefix='/api/')


@api.before_request
def auth():
    """Parse out session token, set request context appropriately.

    Will set g.session_id and g.user
    even if no session information is set this prevents
    erroneous KeyErrors
    """
    token = request.headers.get('Authorization')
    if token is not None:
        if token.startswith('Bearer '):
            token = token[len('Bearer '):]
        elif token.startswith('Token '):
            token = token[len('Token '):]
        try:
            g.user = tokens.get(token)
        except itsdangerous.BadTimeSignature:
            g.user = None
    g.user = None
