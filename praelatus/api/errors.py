"""Error handlers for the internal error types."""

import json
import falcon

from praelatus.models import DuplicateError
from praelatus.models.permissions import PermissionError


def handle_error(ex, req, resp, params):
    """Send error message back with appropriate status code."""
    status = falcon.HTTP_500
    body = {
        'type': ex.__class__.__name__,
        'message': str(ex)
    }

    if isinstance(ex, KeyError):
        status = falcon.HTTP_400
    elif isinstance(ex, json.JSONDecodeError):
        status = falcon.HTTP_400
    elif isinstance(ex, DuplicateError):
        status = falcon.HTTP_409
    elif isinstance(ex, PermissionError):
        status = falcon.HTTP_403
    elif isinstance(ex, falcon.HTTPError):
        status = ex.status
        body['message'] = ex.status

    raise ex
    resp.body = json.dumps(body)
    resp.status = status
