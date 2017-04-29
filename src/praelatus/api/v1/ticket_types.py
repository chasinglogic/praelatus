"""Contains resources for interacting with ticket_types."""

import json
import falcon

import praelatus.lib.ticket_types as ticket_types

from praelatus.lib import session
from praelatus.api.schemas import TicketTypeSchema


class TicketTypesResource():
    """Handlers for the /api/v1/ticketTypes endpoint."""

    def on_post(self, req, resp):
        """
        Create a new ticketType and return the new ticketType object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_types
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        TicketTypeSchema.validate(jsn)
        with session() as db:
            db_res = ticket_types.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all ticket_types the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available ticket_types.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_types
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = ticket_types.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class TicketTypeResource():
    """Handlers for the /api/v1/ticketTypes/{id} endpoint."""

    def on_get(self, req, resp, id):
        """
        Get a single ticketType by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticket_typesid
        """
        user = req.context['user']
        with session() as db:
            db_res = ticket_types.get(db, actioning_user=user, id=id)
            if db_res is None:
                raise falcon.HTTPNotFound()
            resp.body = db_res.to_json()

    def on_put(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-ticket_typesid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = ticket_types.get(db, actioning_user=user, id=id)
            db_res.name = jsn['name']
            ticket_types.update(db, actioning_user=user, ticket_type=db_res)

        resp.body = json.dumps({'message': 'Successfully update ticketType.'})

    def on_delete(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-ticket_typesid
        """
        user = req.context['user']
        with session() as db:
            db_res = ticket_types.get(db, actioning_user=user, id=id)
            ticket_types.delete(db, actioning_user=user, ticket_type=db_res)

        resp.body = json.dumps({'message': 'Successfully deleted ticketType.'})
