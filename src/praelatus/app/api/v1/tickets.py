"""Contains resources for interacting with tickets."""

import praelatus.events as events

from werkzeug.exceptions import NotFound
from flask import jsonify
from flask import request
from flask import g

from praelatus.lib import connection
from praelatus.lib.redis import r
from praelatus.app.api.v1.base import BasicResource
from praelatus.app.api.v1.base import BasicMultiResource
from praelatus.app.api.v1.base import BaseResource


class TicketsResource(BasicMultiResource):
    """Handlers for /api/v1/tickets."""

    def post(self):
        """Create a ticket and return the new ticket object.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-tickets
        """
        jsn = request.get_json()
        if jsn.get('reporter') is None:
            jsn['reporter'] = g.user
        with connection() as db:
            db_res = self.store.new(db, actioning_user=g.user, **jsn)
            return db_res.to_json()


class TicketResource(BasicResource):
    """Handlers for /api/v1/tickets/{ticket_key} endpoint."""

    def get(self, ticket_key):
        """Retrieve a single ticket by ticket key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        with connection() as db:
            db_res = self.store.get(db, actioning_user=g.user,
                                    uid=ticket_key, cached=True)
            if db_res is None:
                raise NotFound()

            if getattr(db_res.__class__, "to_json", None):
                return db_res.to_json()
                return
            return jsonify(db_res)

    def put(self, ticket_key):
        """Update the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        jsn = request.get_json()
        self.schema.validate(jsn)
        with connection() as db:
            orig_tick = self.store.get(db, uid=ticket_key)
            if orig_tick is None:
                raise NotFound()
            # Invalidate the cached version
            r.delete(orig_tick.key)
            self.store.update(db, actioning_user=g.user,
                              project=orig_tick.project,
                              orig_ticket=orig_tick, model=jsn)
            return jsonify({'message': 'Successfully updated ticket.'})

    def delete(self, ticket_key):
        """Delete the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticketsticket_key
        """
        with connection() as db:
            tick = self.store.get(db, actioning_user=g.user, uid=ticket_key)
            if tick is None:
                raise NotFound()
            r.delete(tick.key)
            self.store.delete(db, actioning_user=g.user,
                              project=tick.project, model=tick)
            return jsonify({'message': 'Successfully deleted ticket.'})


class CommentsResource(BasicMultiResource):
    """Handlers for /api/v1/tickets/{ticket_key}/comments endpoint."""

    def __init__(self, store, schema, ticket_store):
        """Add ticket_store to BasicMultiResource as required for comments."""
        super(CommentsResource, self).__init__(store, schema)
        self.ticket_store = ticket_store

    def get(self, ticket_key):
        """Retrieve all comments for the ticket indentified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticket_keycomments
        """
        with connection() as db:
            ticket = self.ticket_store.get(db, actioning_user=g.user,
                                           uid=ticket_key)
            comments = self.store.get_for_ticket(db, actioning_user=g.user,
                                                 project=ticket.project,
                                                 ticket_id=ticket.id)
            return jsonify([x.jsonify() for x in comments])

    def post(self, ticket_key):
        """Create a new comment for the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_keycomments
        """
        jsn = request.get_json()
        jsn['author'] = g.user
        self.schema.validate(jsn)
        with connection() as db:
            ticket = self.ticket_store.get(db, actioning_user=g.user,
                                           uid=ticket_key)
            comment = self.store.new(db, actioning_user=g.user,
                                     project=ticket.project,
                                     ticket_id=ticket.id,
                                     **jsn)
            event = events.Event(g.user, ticket, comment=comment)
            events.send_event(event)
            return comment.to_json()


class CommentResource(BasicResource):
    """Handlers for /api/v1/tickets/{ticket_key}/comments/{id} endpoint."""

    def __init__(self, store, schema, ticket_store):
        """Add ticket_store to BasicMultiResource as required for comments."""
        super(CommentResource, self).__init__(store, schema)
        self.ticket_store = ticket_store

    def put(self, ticket_key, id):
        """Update the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-ticket_keycommentsid
        """
        jsn = request.get_json()
        self.schema.validate(jsn)
        with connection() as db:
            ticket = self.ticket_store.get(db, actioning_user=g.user,
                                           uid=ticket_key)
            comment = self.store.get(db, actioning_user=g.user,
                                     uid=int(id), project=ticket.project)
            comment.body = jsn['body']
            self.store.update(db, comment, actioning_user=g.user,
                              project=ticket.project)

            return jsonify({
                'message': 'Successfully updated comment.'
            })

    def delete(self, ticket_key, id):
        """Delete the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticket_keycommentsid
        """
        with connection() as db:
            ticket = self.ticket_store.get(db, actioning_user=g.user,
                                           uid=ticket_key)
            comment = self.store.get(db, uid=int(id), project=ticket.project)
            self.store.delete(db, model=comment, actioning_user=g.user,
                              project=ticket.project)
            return jsonify({
                'message': 'Successfully deleted comment.'
            })


class TransitionResource(BaseResource):
    """Handlers for /api/v1/tickets/{ticket_key}/transition/{transitiname}."""

    def post(self, ticket_key, transitiname):
        """Perform a transition on ticket indicated by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_keytransition
        """
        with connection() as db:
            ticket = self.store.get(db, actioning_user=g.user,
                                    uid=ticket_key)
            (ticket, transition) = self.store.\
                transititicket(db,
                               actioning_user=g.user,
                               ticket=ticket)
            event = events.Event(g.user, ticket, transition=transition)
            events.send_event(event)
            return jsonify(ticket.jsonify())
