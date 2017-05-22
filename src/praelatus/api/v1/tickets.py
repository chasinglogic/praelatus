"""Contains resources for interacting with tickets."""

import json
import falcon

from praelatus.lib import session
from praelatus.lib.redis import r
from praelatus.api.v1.base import BasicResource
from praelatus.api.v1.base import BasicMultiResource


class TicketsResource(BasicMultiResource):
    """Handlers for /api/v1/tickets."""

    def on_post(self, req, res):
        """Create a ticket and return the new ticket object.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-tickets
        """
        user = req.context.get('user', None)
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        if jsn.get('reporter') is None:
            jsn['reporter'] = user
        with session() as db:
            db_res = self.store.new(db, actioning_user=user, **jsn)
            res.body = db_res.to_json()


class TicketResource(BasicResource):
    """Handlers for /api/v1/tickets/{ticket_key} endpoint."""

    def on_get(self, req, res, ticket_key):
        """Retrieve a single ticket by ticket key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            db_res = self.store.get(db, actioning_user=user,
                                    uid=ticket_key, cached=True)
            if db_res is None:
                raise falcon.HTTPNotFound()

            if getattr(db_res.__class__, "to_json", None):
                res.body = db_res.to_json()
                return
            res.body = json.dumps(db_res)

    def on_put(self, req, res, ticket_key):
        """Update the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(jsn)
        with session() as db:
            orig_tick = self.store.get(db, uid=ticket_key)
            if orig_tick is None:
                raise falcon.HTTPNotFound()
            # Invalidate the cached version
            r.delete(orig_tick.key)
            self.store.update(db, actioning_user=user,
                              project=orig_tick.project,
                              orig_ticket=orig_tick, model=jsn)
            res.body = json.dumps({'message': 'Successfully updated ticket.'})

    def on_delete(self, req, res, ticket_key):
        """Delete the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            tick = self.store.get(db, actioning_user=user, uid=ticket_key)
            if tick is None:
                raise falcon.HTTPNotFound()
            r.delete(tick.key)
            self.store.delete(db, actioning_user=user,
                              project=tick.project, model=tick)
            res.body = json.dumps({'message': 'Successfully deleted ticket.'})


class CommentsResource(BasicMultiResource):
    """Handlers for /api/v1/tickets/{ticket_key}/comments endpoint."""

    def __init__(self, store, schema, ticket_store):
        """Add ticket_store to BasicMultiResource as required for comments."""
        super(CommentsResource, self).__init__(store, schema)
        self.ticket_store = ticket_store

    def on_get(self, req, res, ticket_key):
        """Retrieve all comments for the ticket indentified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticket_keycomments
        """
        user = req.context['user']
        with session() as db:
            ticket = self.ticket_store.get(db, actioning_user=user,
                                           uid=ticket_key)
            comments = self.store.get_for_ticket(db, actioning_user=user,
                                                 project=ticket.project,
                                                 ticket_uid=ticket.id)
            res.body = json.dumps([x.clean_dict() for x in comments])

    def on_post(self, req, res, ticket_key):
        """Create a new comment for the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_keycomments
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        jsn['author'] = user
        self.schema.validate(jsn)
        with session() as db:
            ticket = self.ticket_store.get(db, actioning_user=user,
                                           uid=ticket_key)
            comment = self.store.new(db, actioning_user=user,
                                     project=ticket.project,
                                     ticket_id=ticket.id,
                                     **jsn)
            res.body = comment.to_json()


class CommentResource(BasicResource):
    """Handlers for /api/v1/tickets/{ticket_key}/comments/{id} endpoint."""

    def __init__(self, store, schema, ticket_store):
        """Add ticket_store to BasicMultiResource as required for comments."""
        super(CommentResource, self).__init__(store, schema)
        self.ticket_store = ticket_store

    def on_put(self, req, res, ticket_key, id):
        """Update the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-ticket_keycommentsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        self.schema.validate(jsn)
        with session() as db:
            ticket = self.ticket_store.get(db, actioning_user=user,
                                           uid=ticket_key)
            comment = self.store.get(db, actioning_user=user,
                                     uid=int(id), project=ticket.project)
            comment.body = jsn['body']
            self.store.update(db, comment, actioning_user=user,
                              project=ticket.project)

            res.body = json.dumps({
                'message': 'Successfully updated comment.'
            })

    def on_delete(self, req, res, ticket_key, id):
        """Delete the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticket_keycommentsid
        """
        user = req.context['user']
        with session() as db:
            ticket = self.ticket_store.get(db, actioning_user=user,
                                           uid=ticket_key)
            comment = self.store.get(db, uid=int(id), project=ticket.project)
            self.store.delete(db, model=comment, actioning_user=user,
                              project=ticket.project)
            res.body = json.dumps({
                'message': 'Successfully deleted comment.'
            })


class TransitionResource:
    """Handlers for /api/v1/tickets/{ticket_key}/transition."""

    def on_post(self, req, res, ticket_key):
        """Perform a transition on ticket indicated by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_keytransition
        """
        user = req.context['user']
        transition = req.get_param('name')
        return
