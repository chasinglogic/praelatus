"""
Contains functions for interacting with projects.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy import or_

from praelatus.lib.utils import rollback
from praelatus.lib.permissions import permission_required, add_permission_query
from praelatus.models import Project
from praelatus.models import User
from praelatus.models import Role
from praelatus.models import UserRoles


def get(db, key=None, id=None, name=None, filter=None, actioning_user=None):
    """
    Get projects from the database.

    If the keyword arguments id, name, or key are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    actioning_user -- the user requesting the project (default None)
    id -- database id (default None)
    key -- the project key (default None)
    name -- the project name (default None)
    filter -- a pattern to search through projects with (default None)
    """
    query = db.query(Project).join(User)

    if key is not None:
        query = query.filter(Project.key == key)

    if id is not None:
        query = query.filter(Project.id == id)

    if name is not None:
        query = query.filter(Project.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(
            or_(
                Project.name.like(pattern),
                Project.key.like(pattern),
                User.username.like(pattern),
                User.full_name.like(pattern)
            )
        )

    query = add_permission_query(db, query, actioning_user, 'VIEW_PROJECT')

    if any([key, id]):
        return query.first()
    return query.order_by(Project.key).all()


@rollback
def new(db, **kwargs):
    """
    Create a new project in the database then return that project.

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
    new_project = Project(
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
                first())
        ]

    permission_scheme = kwargs.get('permission_scheme', {})
    new_project.permission_scheme_id = permission_scheme.get('id', 1)

    db.add(new_project)
    db.commit()
    return new_project


@rollback
@permission_required('ADMIN_PROJECT')
def update(db, project=None, actioning_user=None):
    """
    Update the given project in the database.

    project must be a Project class instance.
    """
    db.add(project)
    db.commit()


@rollback
@permission_required('ADMIN_PROJECT')
def delete(db, project=None, actioning_user=None):
    """
    Remove the given project from the database.

    project must be a Project class instance.
    """
    db.delete(project)
    db.commit()
