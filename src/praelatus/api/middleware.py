"""Contains our custom middleware for Praelatus."""

from datetime import timedelta
from datetime import datetime

import praelatus.lib.sessions as sessions


class AuthMiddleware():
    """Checks for authentication info on the request."""

    def process_request(self, req, resp):
        """
        Parse out session token, set request context appropriately.

        Will set req.context['session_id'] and req.context['user']
        even if no session information is set this prevents
        erroneous KeyErrors
        """
        token = req.get_header('Authorization')

        if token is None:
            token = req.cookies.get('PRAE_SESSION')
        elif token.startswith('Bearer '):
            token = token[len('Bearer '):]
        elif token.startswith('Token '):
            token = token[len('Token '):]

        if token is None:
            req.context['session_id'] = None
            req.context['user'] = None
        else:
            req.context['session_id'] = token
            req.context['user'] = sessions.get(token)


class LogMiddleware():
    """Log requests and performance information used for debugging."""

    def __init__(self, logger):
        """Set self.logger to a logger which is any writeable."""
        self.logger = logger

    def process_request(self, req, resp):
        """Set start_time on req.context."""
        req.context['start_time'] = datetime.now()

    def process_response(self, req, resp, resource, req_succeeded):
        """Log response time and other info about response."""
        resp_time = datetime.now() - req.context['start_time']
        resp_time = resp_time / timedelta(milliseconds=1)
        print("[%s] %s %s" % (req_succeeded, req.uri, resp_time))
