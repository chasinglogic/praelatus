"""Contains resources for interacting with tickets."""

import json
import falcon

import praelatus.lib.tickets as tickets


class TicketsResource():
    """Handlers for /api/v1/tickets."""

    def on_get(self, req, resp):
        """Return all tickets as JSON."""
        user = req.context['user']
