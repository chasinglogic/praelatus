from functools import wraps
from sqlalchemy import or_, and_
from sqlalchemy.orm import joinedload
from praelatus.lib.utils import rollback
from praelatus.models import (PermissionScheme, Role, Project,
                              PermissionSchemePermissions,
                              Permission, UserRoles, User)


def get(db, id=None, name=None, filter=None, actioning_user=None):
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
        return None

    query = db.query(PermissionScheme).\
        options(joinedload(PermissionSchemePermissions))

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


@rollback
def new(db, actioning_user=None, **kwargs):
    try:
        if (actioning_user is None or
           not is_system_admin(db, actioning_user)):
            raise Exception('permission denied')

        new_scheme = PermissionScheme(
            name=kwargs['name'],
            description=kwargs.get('description', '')
        )

        db.add(new_scheme)

        permissions = []

        for role_name, perm_name in permissions:
            role = db.query(Role).filter_by(name=role_name).first()
            permission = db.query(Permission).filter_by(name=perm_name).first()

            perm_scheme_perm = PermissionSchemePermissions(
                permission_scheme_id=new_scheme.id,
                role_id=role.id,
                permission_id=permission.id
            )

            permissions.add(perm_scheme_perm)

        db.add_all(permissions)
        db.commit()
    except KeyError as e:
        raise Exception('Missing key ' + str(e.args[0]))


@rollback
def update(db, permission_scheme=None, actioning_user=None):
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
            raise Exception('permission denied')

    db.add(permission_scheme)
    db.commit(0)


@rollback
def delete(db, permission_scheme=None, actioning_user=None):
    if (actioning_user is None or
       not is_system_admin(db, actioning_user)):
            raise Exception('permission denied')

    db.delete(permission_scheme)
    db.commit(0)


def is_system_admin(db, user):
    return db.query(User).get(user.id).first().is_admin


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

            if has_permission(db, permission, project, actioning_user):
                return fn(*args, **kwargs)
            raise Exception('permission denied')
        return wrapper
    return decorator


def has_permission(db, permission, project, actioning_user):
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
        return False
    return True


def add_permission_query(db, query, actioning_user, permission_name):
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
