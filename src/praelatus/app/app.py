"""The global flask app object."""

import flask
import time
import logging
import json
import jsonschema

import praelatus.lib.tokens as tokens

from werkzeug.exceptions import HTTPException
from flask import jsonify
from flask import request
from flask import g

from praelatus.models import DuplicateError
from praelatus.models.permissions import PermissionError
from praelatus.app.api.blueprint import api

# Fix python 3.4 to 3.5 compatibility
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

app = flask.Flask('praelatus')
app.register_blueprint(api)


@app.before_request
def start_time():
    """Set start time for request."""
    g.start = time.time()


@app.after_request
def log_resp_time(response):
    """Log out the response time and status."""
    logging.debug('[%s] %d %s %d' %
                  (request.method, response.status_code,
                   request.path, g.start - time.time()))
    return response


@app.before_request
def auth():
    """Parse out session token, set request context appropriately.

    Will set g.session_id and g.user
    even if no session information is set this prevents
    erroneous KeyErrors
    """
    token = request.headers.get('Authorization')

    if token is None:
        token = request.cookies.get('PRAE_SESSION')
    elif token.startswith('Bearer '):
        token = token[len('Bearer '):]
    elif token.startswith('Token '):
        token = token[len('Token '):]

    if token is None:
        g.session_id = None
        g.user = None
    else:
        g.session_id = token
        g.user = tokens.get(token)


@app.errorhandler(Exception)
@app.errorhandler(404)
@app.errorhandler(405)
@app.errorhandler(400)
def handle_error(ex):
    """Handle errors accordingly."""
    print(ex)
    if request.path.startswith('/api'):
        return handle_api_error(ex)
    else:
        raise ex


def handle_api_error(ex):
    """Send error message back with appropriate status code."""
    status = 500
    body = {
        'type': ex.__class__.__name__,
        'message': str(ex)
    }

    if (
            isinstance(ex, KeyError) or
            isinstance(ex, json.JSONDecodeError) or
            isinstance(ex, jsonschema.ValidationError)
    ):
        status = 400
    elif isinstance(ex, DuplicateError):
        status = 409
    elif isinstance(ex, PermissionError):
        status = 403
    elif isinstance(ex, HTTPException):
        status = ex.code
        body['message'] = __get_message(ex.code)

    resp = jsonify(body)
    resp.status_code = status
    resp.headers['Content-Type'] = 'application/json'
    return resp


def __get_message(code):
    """Return the appropriate JSON body for the given status code."""
    if code == 404:
        return 'not found'
    elif code == 401:
        return 'unauthorized'
    elif code == 403:
        return 'forbidden'
    elif code == 405:
        return 'method not allowed'
    elif code == 400:
        return 'bad request'
    return 'unknown error'
