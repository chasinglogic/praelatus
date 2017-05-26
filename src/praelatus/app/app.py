"""The global flask app object."""

import flask
import time
import logging

import praelatus.lib.tokens as tokens

from flask import g
from flask import request

from praelatus.app.api import add_api_routes

app = flask.Flask('praelatus')
add_api_routes(app)


@app.before_request
def start_time():
    g.start = time.time()


@app.after_request
def log_resp_time(response):
    logging.info('[%s] %d %s %d' %
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
