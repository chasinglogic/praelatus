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
            print('No token present')
            req.context['session_id'] = None
            req.context['user'] = None
        else:
            print('Found token')
            req.context['session_id'] = token
            req.context['user'] = sessions.get(token)
            print('user', req.context['user'])
