from praelatus.lib.utils import rollback, add_permission_query
from praelatus.lib.utils import check_permission
from praelatus.models.projects import Project
from praelatus.models.users import User
from sqlalchemy import or_


def get(db, key=None, id=None, filter=None, actioning_user=None):
    """get gets projects from the database, if key or id are given one
    project is returned otherwise if filter is specified it will
    return all projects which match the given filter."""
    query = db.query(Project).join(User)

    if key is not None:
        query = query.filter(Project.key == key)

    if id is not None:
        query = query.filter(Project.id == id)

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
    """new will create a new project in the database"""
    try:
        lead = kwargs.get('lead')
        permission_scheme = kwargs.get('permission_scheme')

        new_project = Project(
                key=kwargs['key'],
                homepage=kwargs.get('homepage'),
                repo=kwargs.get('repo'),
                icon_url=kwargs.get('icon_url'),
                name=kwargs['name']
        )

        if lead is not None:
            new_project.lead_id = lead.id

        if permission_scheme is not None:
            new_project.permission_scheme_id = permission_scheme.id
        else:
            # The default permission scheme should always be id 1
            new_project.perimssion_scheme_id = 1

        db.add(new_project)
        db.commit()
        return new_project
    except KeyError as e:
        raise Exception('Missing key ' + str(e.args[0]))


@rollback
@check_permission('ADMIN_PROJECT')
def update(db, project=None, actioning_user=None):
    db.add(project)
    db.commit()


@rollback
@check_permission('ADMIN_PROJECT')
def delete(db, project=None, actioning_user=None):
    db.delete(project)
    db.commit()
