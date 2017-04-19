"""Error handlers for the internal error types."""

import json
import falcon


def handle_generic_error(ex, req, resp, params):
    """Send an ISE on an uncaught base Exception."""
    resp.body = json.dumps({'message': ex.message})
    resp.status = falcon.HTTP_500


def handle_permission_error(ex, req, resp, params):
    """Implement error handling for PermissionErrors in our falcon.API."""
    resp.body = json.dumps({'message': ex.message})
    resp.status = falcon.HTTP_403


def handle_key_error(ex, req, resp, params):
    """Implement error handling for KeyErrors in our falcon.API."""
    resp.body = json.dumps({'message': ex.message})
    resp.status = falcon.HTTP_400
