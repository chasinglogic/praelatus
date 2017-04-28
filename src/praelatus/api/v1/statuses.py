"""Contains resources for interacting with statuses."""

import json

import praelatus.lib.statuses as statuses

from praelatus.lib import session
from praelatus.api.schemas import StatusSchema


class StatusesResource():
    """Handlers for the /api/v1/statuses endpoint."""

    def on_post(self, req, resp):
        """
        Create a new ticketType and return the new ticketType object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-statuses
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        StatusSchema.validate(jsn)
        with session() as db:
            db_res = statuses.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all statuses the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available statuses.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-statuses
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = statuses.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class StatusResource():
    """Handlers for the /api/v1/statuses/{id} endpoint."""

    def on_get(self, req, resp, id):
        """
        Get a single ticketType by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-statusesid
        """
        user = req.context['user']
        with session() as db:
            db_res = statuses.get(db, actioning_user=user, id=id)
            resp.body = db_res.to_json()

    def on_put(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-statusesid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = statuses.get(db, actioning_user=user, id=id)
            db_res.homepage = jsn.get('homepage', '')
            db_res.icon_url = jsn.get('icon_url', '')
            db_res.repo = jsn.get('repo', '')
            db_res.name = jsn['name']
            db_res.id = jsn['id']
            if db_res.lead.id != jsn['lead']['id']:
                db_res.lead_id = jsn['lead']['id']
            statuses.update(db, actioning_user=user, ticketType=db_res)

        resp.body = json.dumps({'message': 'Successfully update ticketType.'})

    def on_delete(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-statusesid
        """
        user = req.context['user']
        with session() as db:
            db_res = statuses.get(db, actioning_user=user, id=id)
            statuses.delete(db, actioning_user=user, ticketType=db_res)

        resp.body = json.dumps({'message': 'Successfully deleted ticketType.'})
