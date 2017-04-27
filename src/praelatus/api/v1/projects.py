"""Contains resources for interacting with projects."""

import json
import falcon

import praelatus.lib.projects as projects

from praelatus.lib import session
from praelatus.api.schemas import ProjectSchema


class ProjectsResource():
    """Handlers for the /api/v1/projects endpoint."""

    def on_post(self, req, resp):
        """
        Create a new project and return the new project object.

        You must be a system administrator to use this endpoint.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-projects
        """
        user = req.context['user']
        jsn = json.loads(req.bounded_stream.read().decode('utf-8'))
        ProjectSchema.validate(jsn)
        with session() as db:
            db_res = projects.new(db, actioning_user=user, **jsn)
            resp.body = db_res.to_json()

    def on_get(self, req, resp):
        """
        Get all projects the current user has access to.

        Accepts an optional query parameter 'filter' which can be used
        to search through available projects.

        API Documentation:
        https://docs.praelatus.io/API/Reference/#post-projects
        """
        user = req.context['user']
        query = req.params.get('filter', '*')
        with session() as db:
            db_res = projects.get(db, actioning_user=user, filter=query)
            resp.body = json.dumps([p.clean_dict() for p in db_res])


class ProjectResource():
    """Handlers for the /api/v1/projects/{key} endpoint."""

    def on_get(self, req, resp, key);
    def on_put(self, req, resp, key);
    def on_delete(self, req, resp, key);
