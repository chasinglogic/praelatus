"""Contains resources for interacting with fields."""

import json

import praelatus.lib.fields as fields

from praelatus.lib import session
from praelatus.api.schemas import FieldSchema


class FieldsResource():
    """Handlers for the /api/v1/fields endpoint."""

    def on_post(self, req, resp):
        """
        Create a new ticketType and return the new ticketType object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-fields
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        FieldSchema.validate(jsn)
        with session() as db:
            db_res = fields.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all fields the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available fields.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-fields
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = fields.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class FieldResource():
    """Handlers for the /api/v1/fields/{id} endpoint."""

    def on_get(self, req, resp, id):
        """
        Get a single ticketType by id.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-fieldsid
        """
        user = req.context['user']
        with session() as db:
            db_res = fields.get(db, actioning_user=user, id=id)
            resp.body = db_res.to_json()

    def on_put(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-fieldsid
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = fields.get(db, actioning_user=user, id=id)
            db_res.homepage = jsn.get('homepage', '')
            db_res.icon_url = jsn.get('icon_url', '')
            db_res.repo = jsn.get('repo', '')
            db_res.name = jsn['name']
            db_res.id = jsn['id']
            if db_res.lead.id != jsn['lead']['id']:
                db_res.lead_id = jsn['lead']['id']
            fields.update(db, actioning_user=user, ticketType=db_res)

        resp.body = json.dumps({'message': 'Successfully update ticketType.'})

    def on_delete(self, req, resp, id):
        """
        Update the ticketType indicated by id.

        You must have the ADMIN_TICKETTYPE permission to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-fieldsid
        """
        user = req.context['user']
        with session() as db:
            db_res = fields.get(db, actioning_user=user, id=id)
            fields.delete(db, actioning_user=user, ticketType=db_res)

        resp.body = json.dumps({'message': 'Successfully deleted ticketType.'})
