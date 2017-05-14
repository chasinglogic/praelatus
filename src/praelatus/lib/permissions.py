"""Contains functions for interacting with roles, and permission schemes.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from functools import wraps
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from praelatus.models import PermissionScheme
from praelatus.models import Role
from praelatus.models import Project
from praelatus.models import PermissionSchemePermissions
from praelatus.models import Permission
from praelatus.models.permissions import PermissionError
from praelatus.models import UserRoles
from praelatus.models import User


def is_system_admin(db, user):
    """Check if user is a system administrator."""
    query = db.query(User)
    if type(user) is dict:
        query = query.filter_by(id=user.get('id', 0))
    else:
        query = query.filter_by(id=user.id)
    return query.first().is_admin


def sys_admin_required(fn):
    """Check if actioning_user is a system administrator."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        actioning_user = kwargs.pop('actioning_user', None)
        if (actioning_user is None or
           not is_system_admin(args[1], actioning_user)):
            raise PermissionError('you must be a system administrator')

        return fn(*args, **kwargs)
    return wrapper


def permission_required(permission):
    """Check if the actioning_user has permission."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            project = kwargs.get('project')
            if project is None:
                raise Exception('project is required to check permissions')

            actioning_user = kwargs.pop('actioning_user', None)
            db = args[1]

            if has_permission(db, permission, project, actioning_user):
                return fn(*args, **kwargs)
            raise PermissionError('permission denied')
        return wrapper
    return decorator


def has_permission(db, permission_name, project, actioning_user):
    """Check if permission is granted to actioning_user on project."""
    query = db.query(Project.id).\
        join(UserRoles).\
        join(User).\
        join(Role).\
        join(PermissionScheme).\
        join(PermissionSchemePermissions).\
        join(Permission)

    if isinstance(project, Project):
        query = query.filter(Project.id == project.id)
    else:
        query = query.filter(Project.id == project['id'])

    if actioning_user is not None and isinstance(actioning_user, User):
        user_id = actioning_user.id
    elif actioning_user is not None:
        user_id = actioning_user.get('id', 0)
    else:
        user_id = 0

    if actioning_user is not None:
        # Check if they're an admin first it's faster this way.
        is_admin = db.query(User.is_admin).filter(User.id == user_id).first()
        if is_admin:
            return True

    query = query.filter(
        Permission.name == permission_name,
        or_(
            Role.name == 'Anonymous',
            UserRoles.user_id == user_id
        ),
    )

    print('query', query)
    if query.first() is None:
        return False
    return True


def add_permission_query(db, query, actioning_user, permission_name):
    """Add the requisite joins and filters to check for permission_name.

    If the Project table is not already joined then this will not work.
    """
    # If they're a sys admin no need to modify the query at all.
    if actioning_user is not None and is_system_admin(db, actioning_user):
        return query

    query = query.join(
        PermissionScheme,
        Project.permission_scheme_id == PermissionScheme.id
    ).join(
        PermissionSchemePermissions,
        Permission
    ).outerjoin(
        Role,
        PermissionSchemePermissions.role_id == Role.id
    ).outerjoin(
        UserRoles,
        UserRoles.project_id == Project.id
    )

    if actioning_user is not None and isinstance(actioning_user, User):
        user_id = actioning_user.id
    elif actioning_user is not None:
        user_id = actioning_user.get('id', 0)
    else:
        user_id = 0

    return query.filter(
        Permission.name == permission_name,
        or_(
            UserRoles.user_id == user_id,
            Role.name == 'Anonymous'
        )
    )
