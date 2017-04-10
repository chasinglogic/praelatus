"""Contains utility functions and decorators for use in lib"""
from functools import wraps
from sqlalchemy import or_, and_
from praelatus.models import (PermissionScheme, Role, Project,
                              PermissionSchemePermissions,
                              Permission, UserRoles, User)


def rollback(fn):
    """rollback is a decorator which on an uncaught exception will
    rollback the db session"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            args[0].rollback()
            raise e

    return wrapper


def permission_required(permission):
    """permission_required will check if the actioning_user has the
       'permission' indicated by the parameter.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            project = kwargs.get('project')
            if project is None:
                raise Exception('project is required to check permissions')

            actioning_user = kwargs.get('actioning_user')
            db = *args[0]

            query = db.query(Project.id).\
                join(UserRoles).\
                join(Role).\
                join(PermissionScheme).\
                join(PermissionSchemePermissions).\
                join(Permission).\
                filter(Project.id == project)

            if actioning_user is not None:
                query = query.filter(
                    or_(
                        db.query(User.is_admin).
                        filter(User.id == actioning_user.id).
                        subquery('admin').as_scalar(),
                        and_(
                            Permission.name == permission,
                            or_(
                                Role.name == 'Anonymous',
                                UserRoles.user_id == actioning_user.id
                            ),
                        )
                    )
                )
            else:
                query = query.filter(
                    Permission.name == permission,
                    Role.name == 'Anonymous'
                )

            if query.first() is None:
                raise Exception('permission denied')

            return fn(*args, **kwargs)
        return wrapper
    return decorator


def permission_check(db, query, actioning_user, permission_name):
    """If Projects is already joined to the given query, permission_check
       will add the requisite joins and filters to check for the
       permission permission_name
    """
    query = query.join(
        PermissionScheme,
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

    if actioning_user is not None:
        query = query.filter(
            or_(
                db.query(User.is_admin).
                filter(User.id == actioning_user.id).
                subquery('admin').as_scalar(),
                and_(
                    UserRoles.user_id == actioning_user.id,
                    Permission.name == permission_name
                )
            )
        )

        print(str(query))

    else:
        query = query.filter(
            and_(
                Permission.name == permission_name,
                Role.name == 'Anonymous'
            )
        )

    return query
