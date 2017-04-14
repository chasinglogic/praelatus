"""
Contains methods for interacting with labels.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from praelatus.models import Label, Ticket
from praelatus.lib.utils import rollback
from sqlalchemy.orm import joinedload


def get(db, id=None, name=None, filter=None, preload_tickets=False):

    """
    Get projects from the database.

    If the keyword arguments id, name, or key are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    keyword arguments:
    actioning_user -- the user requesting the project (default None)
    id -- database id (default None)
    key -- the project key (default None)
    name -- the project name (default None)
    filter -- a pattern to search through projects with (default None)
    """

    query = db.query(Label)

    if id is not None:
        query = query.filter(Label.id == id)

    if name is not None:
        query = query.filter(Label.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Label.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(Label.name).all()


@rollback
def new(db, **kwargs):
    try:
        new_label = Label(
            name=kwargs['name'],
        )
        db.add(new_label)
        db.commit()
        return new_label
    except KeyError:
        raise Exception('Missing key name')


@rollback
def update(db, label):
    db.add(label)
    db.commit()


@rollback
def delete(db, label):
    db.delete(label)
    db.commit()
