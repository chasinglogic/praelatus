"""Contains resources for interacting with tickets."""

import json
import falcon

from praelatus.lib import session
import praelatus.lib.tickets as tickets
from praelatus.api.schemas import TicketSchema


class TicketsResource():
    """Handlers for /api/v1/tickets."""

    def on_post(self, req, resp):
        """
        Create a ticket and return the new ticket object.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-tickets
        """
        user = req.context.get('user', None)
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        if jsn.get('reporter') is None:
            jsn['reporter'] = user
        with session() as db:
            db_res = tickets.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Return all tickets the current user has access to.
        
        Accepts the query parameter filter which searches through
        tickets on the instance. This will eventually be replaced with
        a query language but for now supports simple text searching.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-tickets
        """
        user = req.context['user']
        query = req.params.get('filter', '*')

        with session() as db:
            db_res = tickets.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([t.clean_dict() for t in db_res])


class TicketResource():
    """Handlers for /api/v1/tickets/{key} endpoint."""

    def on_get(self, req, resp, key):
        """
        Retrieve a single ticket by ticket key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            db_res = tickets.get(db, actioning_user=user, key=key)
            resp.body = db_res.to_json()

    def on_put(self, req, resp, key):
        """
        Update the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        TicketSchema.validate(jsn)
        with session() as db:
            orig_tick = tickets.get(db, key=key)
            if orig_tick is None:
                raise falcon.HTTPNotFound()
            tickets.update(db, actioning_user=user,
                           orig_ticket=orig_tick, ticket=jsn)

    def on_delete(self, req, resp, key):
        """
        Delete the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            tick = tickets.get(db, actioning_user=user, key=key)
            if tick is None:
                raise falcon.HTTPNotFound()
            tickets.delete(db, actioning_user=user,
                           project=tick.project, ticket=tick)
        resp.body = json.dumps({'message': 'Successfully deleted ticket.'})
