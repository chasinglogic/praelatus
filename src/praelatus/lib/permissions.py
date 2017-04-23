"""
Contains functions for interacting with roles, and permission schemes.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from functools import wraps
from sqlalchemy import or_
from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from praelatus.models import PermissionScheme
from praelatus.models import Role
from praelatus.models import Project
from praelatus.models import PermissionSchemePermissions
from praelatus.models import Permission
from praelatus.models.permissions import PermissionError
from praelatus.models import UserRoles
from praelatus.models import User



def get(db, id=None, name=None, filter=None, actioning_user=None):
    """
    Get permission schemes from the database.

    If the keyword arguments id or name are specified returns a single
    sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    actioning_user -- the user requesting the permission scheme
    id -- database id
    name -- the permission scheme name
    filter -- a pattern to search through permission schemes with
    """
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
        return None

    query = db.query(PermissionScheme).\
        options(joinedload('permissions'))

    if id is not None:
        query = query.filter(PermissionScheme.id == id)

    if name is not None:
        query = query.filter(PermissionScheme.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(
            PermissionScheme.name.like(pattern)
        )

    if any([id, name]):
        return query.first()
    return query.order_by(PermissionScheme.name).all()



def new(db, actioning_user=None, **kwargs):
    """
    Create a new permission scheme in the database then return it.

    The kwargs are parsed such that if a json representation of a
    permission scheme is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    namm -- the permission scheme name
    description -- the permission scheme's description
    actioning_user -- the User creating the permission scheme
    """
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
        raise Exception('permission denied')

    new_scheme = PermissionScheme(
        name=kwargs['name'],
        description=kwargs.get('description', '')
    )

    permissions = kwargs['permissions']
    for role_name, perms in permissions.items():
        role = db.query(Role).filter_by(name=role_name).first()
        for perm in perms:
            permission = db.query(Permission).filter_by(name=perm).first()
            perm_scheme_perm = PermissionSchemePermissions(
                role_id=role.id,
                permission_id=permission.id
            )

            new_scheme.permissions.append(perm_scheme_perm)

    db.add(new_scheme)
    db.commit()

    return new_scheme



def update(db, permission_scheme=None, actioning_user=None):
    """
    Update the permission scheme in the database.

    permission_scheme must be a PermissionScheme class instance.
    """
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
            raise Exception('permission denied')

    db.add(permission_scheme)
    db.commit()



def delete(db, permission_scheme=None, actioning_user=None):
    """
    Remove the permission scheme from the database.

    permission_scheme must be a PermissionScheme class instance.
    """
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
            raise Exception('permission denied')

    db.delete(permission_scheme)
    db.commit()


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
        actioning_user = kwargs.get('actioning_user')
        if (actioning_user is None or
           not is_system_admin(args[0], actioning_user)):
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

            actioning_user = kwargs.get('actioning_user')
            db = args[0]

            if has_permission(db, permission, project, actioning_user):
                return fn(*args, **kwargs)
            raise Exception('permission denied')
        return wrapper
    return decorator


def has_permission(db, permission_name, project, actioning_user):
    """Check if permission is granted to actioning_user on project."""
    query = db.query(Project.id).\
        join(UserRoles).\
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

    if actioning_user is not None:
        query = query.filter(
            or_(
                db.query(User.is_admin).
                filter(User.id == user_id).
                subquery('admin').as_scalar(),
                and_(
                    Permission.name == permission_name,
                    or_(
                        Role.name == 'Anonymous',
                        UserRoles.user_id == user_id
                    ),
                )
            )
        )
    else:
        query = query.filter(
            Permission.name == permission_name,
            Role.name == 'Anonymous'
        )

    if query.first() is None:
        return False
    return True


def add_permission_query(db, query, actioning_user, permission_name):
    """
    Add the requisite joins and filters to check for permission_name.

    If the Project table is not already joined then this will not work.
    """
    query = query.join(
        PermissionScheme,
        Project.permission_scheme_id == PermissionScheme.id
    )

    query = query.join(
        PermissionSchemePermissions,
        Permission
    )

    query = query.outerjoin(
        Role,
        PermissionSchemePermissions.role_id == Role.id
    )

    query = query.outerjoin(
        UserRoles,
        UserRoles.project_id == Project.id
    )

    if actioning_user is not None and isinstance(actioning_user, User):
        user_id = actioning_user.id
    elif actioning_user is not None:
        user_id = actioning_user.get('id', 0)

    if actioning_user is not None:
        query = query.filter(
            or_(
                db.query(User.is_admin).
                filter(User.id == user_id).
                subquery('admin').as_scalar(),
                and_(
                    UserRoles.user_id == user_id,
                    Permission.name == permission_name
                )
            )
        )
    else:
        query = query.filter(
            and_(
                Permission.name == permission_name,
                Role.name == 'Anonymous'
            )
        )

    return query
