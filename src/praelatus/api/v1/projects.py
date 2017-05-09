"""Resources for the /api/v1/projects endpoints."""

import json
import falcon

import praelatus.lib.projects as projects
import praelatus.lib.tickets as tickets

from praelatus.lib import session
from praelatus.api.schemas import ProjectSchema


class ProjectTicketsResource:
    """Handlers for the /api/v1/projects/{key}/tickets."""

    def on_get(self, req, res, key):
        """Get all tickets for project with key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-projectskeytickets
        """
        user = req.context['user']
        with session() as db:
            db_res = tickets.get(db, actioning_user=user, project_key=key)
            res.body = json.dumps([t.clean_dict() for t in db_res])


class ProjectResource:
    """Handlers for the /api/v1/projects/{key} endpoint."""
    lib = projects
    schema = ProjectSchema
    model_name = 'project'

    def on_get(self, req, res, key):
        """Get a single model by key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#get-modelskey

        """
        user = req.context['user']
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, key=key)
            if db_res is None:
                raise falcon.HTTPNotFound()
            res.body = db_res.to_json()

    def on_put(self, req, res, key):
        """Update the model indicated by key.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelskey
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, key=key)
            db_res.name = jsn['name']
            kwa = {}
            kwa[self.model_name] = db_res
            self.lib.update(db, actioning_user=user, **kwa)

        res.body = json.dumps({
            'message': 'Successfully updated %s.' % self.model_name
        })

    def on_delete(self, req, res, key):
        """Update the model indicated by key.

        You must have the ADMIN_TICKETTYPE permission to use this
        endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#put-modelskey
        """
        user = req.context['user']
        with session() as db:
            db_res = self.lib.get(db, actioning_user=user, key=key)
            kwa = {}
            kwa[self.model_name] = db_res
            self.lib.delete(db, actioning_user=user, **kwa)

        res.body = json.dumps({
            'message': 'Successfully deleted %s.' % self.model_name
        })
