"""The global flask app object."""

import markdown
import json
import jsonschema
import sys
import itsdangerous

import praelatus.lib.tokens as tokens

from jinja2 import Markup
from logging import StreamHandler
from logging import Formatter
from werkzeug.exceptions import HTTPException
from flask import url_for
from flask import Flask
from flask import redirect
from flask import jsonify
from flask import request
from flask import g

from praelatus.models import DuplicateError
from praelatus.lib.tokens import get_secret_key
from praelatus.models.permissions import PermissionError
from praelatus.config import config
from praelatus.app.api import api
from praelatus.app.ui import ui


# Configure logging
fmt = Formatter('[%(asctime)s] [PRAE] [%(levelname)s] %(message)s')
stdo = StreamHandler(sys.stdout)
stdo.setFormatter(fmt)

# Fix python 3.4 to 3.5 compatibility
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

app = Flask('praelatus')
app.secret_key = get_secret_key()
app.register_blueprint(api)
app.register_blueprint(ui)


# Add markdown filter to templates.
md = markdown.Markdown()
app.jinja_env.filters['markdown'] = lambda text: Markup(md.convert(text))


# Fix bad names.
def humanize(text):
    """Take snake_case string and make it human readable."""
    return ' '.join([s.capitalize() for s in text.split('_')])


app.jinja_env.filters['humanize'] = humanize

loggers = [app.logger]
for l in loggers:
    l.addHandler(stdo)
    l.setLevel(config.log_level)


@app.after_request
def log_resp_time(response):
    """Log out the response time and status."""
    app.logger.debug('[%s] %d %s' %
                     (request.method, response.status_code, request.path))
    return response


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
        return handle_ui_error(ex)


def handle_ui_error(ex):
    """Handle errors appropriately in the UI."""
    if isinstance(ex, itsdangerous.BadTimeSignature):
        return redirect(url_for('login'))
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
