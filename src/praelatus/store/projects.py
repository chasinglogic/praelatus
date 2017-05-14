"""Contains definition for the ProjectStore class."""

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from praelatus.models import Project
from praelatus.models import User
from praelatus.models import UserRoles
from praelatus.models import DuplicateError
from praelatus.models import Role
from praelatus.lib.permissions import sys_admin_required
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import add_permission_query
from praelatus.store.store import Store
from praelatus.store.workflows import store as workflow_store


class ProjectStore(Store):
    """Stores and retrieves Projects."""

    def __init__(self, model, workflow_store):
        """Model should be the Project model.

        workflow_store should be a WorkflowStore.
        """
        self.model = model
        self.workflow_store = workflow_store

    def get(self, db, uid=None, id=None, name=None,
            actioning_user=None, **kwargs):
        """Get a single project from the database."""
        query = db.query(Project)
        query = add_permission_query(db, query,
                                     actioning_user, 'VIEW_PROJECT')
        if uid is not None:
            query = query.filter(Project.key == uid)
        elif id is not None:
            query = query.filter(Project.id == id)
        elif name is not None:
            query = query.filter(Project.name == name)
        else:
            return None
        return query.first()

    def search(self, db, search, actioning_user=None, **kwargs):
        """Search through projects and return all matches."""
        pattern = filter.replace('*', '%')
        query = db.query(Project).filter(
            or_(
                Project.name.like(pattern),
                Project.key.like(pattern),
                User.username.like(pattern),
                User.full_name.like(pattern)
            )
        )

        query = add_permission_query(db, query, actioning_user, 'VIEW_PROJECT')
        return query.order_by(Project.key).all()

    @sys_admin_required
    def new(self, db, **kwargs):
        """Create a new project in the database then return that project.

        The kwargs are parsed such that if a json representation of a
        project is provided as expanded kwargs it will be handled
        properly.

        If a required argument is not provided then it raises a KeyError
        indicating which key was missing. Useful for returning HTTP 400
        errors.

        required keyword arguments:
        key -- the project key
        name -- the project name

        optional keyword arguments
        homepage -- the homepage for the project
        repo -- the repository for this projects code
        permission_scheme -- the permission scheme to use for this project
        lead -- the project lead for this project
        """
        new_project = self.model(
            key=kwargs['key'],
            homepage=kwargs.get('homepage'),
            repo=kwargs.get('repo'),
            icon_url=kwargs.get('icon_url'),
            name=kwargs['name']
        )

        lead = kwargs.get('lead')
        if lead is not None:
            new_project.lead_id = lead['id']
            new_project.roles = [
                UserRoles(
                    user_id=lead['id'],
                    role_id=db.
                    query(Role.id).
                    filter_by(name='Administrator').
                    first()),
                UserRoles(
                    user_id=1,
                    role_id=db.
                    query(Role.id).
                    filter_by(name='Anonymous').
                    first())
            ]

        permission_scheme = kwargs.get('permission_scheme', {})
        new_project.permission_scheme_id = permission_scheme.get('id', 1)
        new_project.workflows = [self.workflow_store.get(db, uid=1)]

        try:
            db.add(new_project)
            db.commit()
        except IntegrityError as e:
            raise DuplicateError('That project key or name is already taken.')
        return new_project

    @permission_required('ADMIN_PROJECT')
    def update(self, db, model=None, **kwargs):
        """Update the project in the database."""
        db.add(model)
        db.commit()

    @permission_required('ADMIN_PROJECT')
    def delete(self, db, model=None, **kwargs):
        """Update the project in the database."""
        db.delete(model)
        db.commit()


store = ProjectStore(Project, workflow_store)
