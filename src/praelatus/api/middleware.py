"""Contains our custom middleware for Praelatus."""

import praelatus.lib.sessions as sessions


class ContentTypeMiddleware():
    """Checks Accepts header on requests and sets content-type on response."""

    def process_response(self, req, resp, resource, success):
        """Add Content-Type header when appropriate."""
        resp.set_header('Content-Type', 'application/json')


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
