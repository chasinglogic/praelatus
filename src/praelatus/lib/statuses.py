"""
Contains functions for interacting with statuses.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy.orm import joinedload

from praelatus.models import Status
from praelatus.models import Ticket
from praelatus.lib.utils import rollback
from praelatus.lib.permissions import sys_admin_required


def get(db, id=None, name=None, filter=None, preload_tickets=False):
    """
    Get statuses from the database.

    If the keyword arguments id or name are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- database id (default None)
    name -- the statuse name (default None)
    filter -- a pattern to search through statuses with (default None)
    preload_tickets -- whether to load the tickets associated with
                       this statuse (default False)
    """
    query = db.query(Status)

    if id is not None:
        query = query.filter(Status.id == id)

    if name is not None:
        query = query.filter(Status.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Status.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(Status.name).all()


@rollback
@sys_admin_required
def new(db, actioning_user=None, **kwargs):
    """
    Create a new statuse in the database then returns that statuse.

    The kwargs are parsed such that if a json representation of a
    statuse is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    name -- the status name
    """
    new_status = Status(
        name=kwargs['name'],
    )

    db.add(new_status)
    db.commit()
    return new_status


@rollback
@sys_admin_required
def update(db, actioning_user=None, status=None):
    """
    Update the given statuse in the database.

    statuse must be a Status class instance.
    """
    db.add(status)
    db.commit()


@rollback
@sys_admin_required
def delete(db, actioning_user=None, status=None):
    """
    Remove the given statuse from the database.

    statuse must be a Status class instance.
    """
    db.delete(status)
    db.commit()
