"""Contains resources for interacting with tickets."""

import json
import falcon

import praelatus.lib.tickets as tickets
import praelatus.lib.projects as projects

from praelatus.lib import session
from praelatus.api.schemas import TicketSchema
from praelatus.api.schemas import CommentSchema


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
    """Handlers for /api/v1/tickets/{ticket_key} endpoint."""

    def on_get(self, req, resp, ticket_key):
        """
        Retrieve a single ticket by ticket key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            db_res = tickets.get(db, actioning_user=user, key=ticket_key)
            resp.body = db_res.to_json()

    def on_put(self, req, resp, ticket_key):
        """
        Update the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticketsticket_key
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        TicketSchema.validate(jsn)
        with session() as db:
            orig_tick = tickets.get(db, key=ticket_key)
            if orig_tick is None:
                raise falcon.HTTPNotFound()
            tickets.update(db, actioning_user=user,
                           orig_ticket=orig_tick, ticket=jsn)

    def on_delete(self, req, resp, ticket_key):
        """
        Delete the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticketsticket_key
        """
        user = req.context['user']
        with session() as db:
            tick = tickets.get(db, actioning_user=user, key=ticket_key)
            if tick is None:
                raise falcon.HTTPNotFound()
            tickets.delete(db, actioning_user=user,
                           project=tick.project, ticket=tick)
        resp.body = json.dumps({'message': 'Successfully deleted ticket.'})


class CommentsResource():
    """Handlers for /api/v1/tickets/{ticket_key}/comments endpoint."""

    def on_get(self, req, resp, ticket_key):
        """
        Retrieve all comments for the ticket indentified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-ticket_keycomments
        """
        user = req.context['user']
        with session() as db:
            ticket = tickets.get(db, actioning_user=user, key=ticket_key)
            comments = tickets.get_comments(db, actioning_user=user,
                                            project=ticket.project,
                                            ticket_key=ticket_key)
            resp.body = json.dumps([x.clean_dict() for x in comments])

    def on_post(self, req, resp, ticket_key):
        """
        Create a new comment for the ticket identified by ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-ticket_keycomments
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        jsn['author'] = user
        CommentSchema.validate(jsn)
        with session() as db:
            ticket = tickets.get(db, actioning_user=user, key=ticket_key)
            comment = tickets.add_comment(db, actioning_user=user,
                                          project=ticket.project,
                                          ticket_id=ticket.id,
                                          **jsn)
            resp.body = comment.to_json()


class CommentResource():
    """Handlers for /api/v1/tickets/{ticket_key}/comments/{id} endpoint."""

    def on_put(self, req, resp, ticket_key, id):
        """
        Update the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-ticket_keycommentsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        CommentSchema.validate(jsn)
        with session() as db:
            project = projects.get(db, actioning_user=user,
                                   key=ticket_key.split('-')[0])
            ticket = tickets.get(db, actioning_user=user,
                                 key=ticket_key, project=project)
            comment = tickets.get_comment(db, int(id))
            comment.body = jsn['body']
            tickets.update_comment(db, comment, actioning_user=user,
                                   project=ticket.project)

            resp.body = json.dumps({'message': 'Successfully updated comment.'})

    def on_delete(self, req, resp, ticket_key, id):
        """
        Delete the comment at ID for ticket_key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#delete-ticket_keycommentsid
        """
        user = req.context['user']
        with session() as db:
            project = projects.get(db, actioning_user=user,
                                   key=ticket_key.split('-')[0])
            ticket = tickets.get(db, actioning_user=user,
                                 key=ticket_key, project=project)
            comment = ticket.get_comment(db, int(id))
            tickets.delete_comment(db, comment, actioning_user=user,
                                   project=ticket.project)

            resp.body = json.dumps({'message': 'Successfully deleted comment.'})
