import json
import falcon

from flask import Blueprint
from flask import jsonify
from werkzeug import HTTPException

from praelatus.app.api.v1 import add_v1_routes
from praelatus.models import DuplicateError
from praelatus.models.permissions import PermissionError

# Fix python 3.4 to 3.5 compatibility
if not hasattr(json, 'JSONDecodeError'):
    json.JSONDecodeError = ValueError

api = Blueprint('api', __name__)
add_v1_routes()


@api.errorhandler(Exception)
def handle_error(ex):
    """Send error message back with appropriate status code."""
    status = falcon.HTTP_500
    body = {
        'type': ex.__class__.__name__,
        'message': str(ex)
    }

    if isinstance(ex, KeyError) or isinstance(ex, json.JSONDecodeError):
        status = 400
    elif isinstance(ex, DuplicateError):
        status = 409
    elif isinstance(ex, PermissionError):
        status = 403
    elif isinstance(ex, HTTPException):
        status = ex.code
        body['message'] = ex.description

    resp = jsonify(body)
    resp.status_code = status
    return resp
