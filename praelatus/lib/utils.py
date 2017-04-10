"""Contains utility functions and decorators for use in lib"""
from sqlalchemy import or_, and_
from praelatus.models import (PermissionScheme, Role, Project,
                              PermissionSchemePermissions,
                              Permission, UserRoles)


def rollback(fn):
    """rollback is a decorator which on an uncaught exception will
    rollback the db session"""
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            args[0].rollback()
            raise e

    return wrapper


def permission_check(query, actioning_user, permission_name):
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
