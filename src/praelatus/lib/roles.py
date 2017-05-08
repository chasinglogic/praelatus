"""Contains functions for interacting with roles.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy.orm import joinedload

from praelatus.models import Role
from praelatus.models import UserRoles
from praelatus.models import ProjectRoles
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import sys_admin_required


@sys_admin_required
def get(db, actioning_user=None, id=None, name=None, filter=None):
    """Get roles from the database.

    If the keyword arguments id, or name are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- the role's database id (default None)
    name -- the role's name (default None)
    filter -- a pattern to search through roles with (default None)
    """
    query = db.query(Role)

    if id is not None:
        query = query.filter(Role.id == id)

    if name is not None:
        query = query.filter(Role.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Role.name.like(pattern))

    if any([id, name]):
        return query.first()
    return query.order_by(Role.name).all()


@sys_admin_required
def new(db, **kwargs):
    """Create a new role in the database then return that role.

    The kwargs are parsed such that if a json representation of a
    role is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    name -- the role name
    """
    new_role = Role(name=kwargs['name'])
    db.add(new_role)
    db.commit()
    return new_role


@sys_admin_required
def update(db, role=None, actioning_user=None):
    """Update the given role in the database.

    role must be a Role class instance.
    """
    db.add(role)
    db.commit()


@sys_admin_required
def delete(db, role=None, actioning_user=None):
    """Remove the given role from the database.

    role must be a Role class instance.
    """
    db.delete(role)
    db.commit()


@permission_required('ADMIN_PROJECT')
def get_roles_for_project(db, project=None):
    """Get the UserRoles for the given project.

    This function returns a ProjectRoles instance for the UserRoles retrieved
    for the project.
    """
    return ProjectRoles(
        db.query(UserRoles).
        options(
            joinedload('user'),
            joinedload('role')
        ).
        filter(UserRoles.project_id == project.id).
        all()
    )
