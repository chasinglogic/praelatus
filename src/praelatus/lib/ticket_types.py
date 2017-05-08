"""Contains functions for interacting with ticket_types.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy.orm import joinedload

from praelatus.models import TicketType
from praelatus.models import Ticket
from praelatus.lib.permissions import sys_admin_required


def get(db, actioning_user=None, id=None, name=None, filter=None,
        preload_tickets=False):
    """Get ticket_types from the database.

    If the keyword arguments id or name are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- database id (default None)
    name -- the TicketType name (default None)
    filter -- a pattern to search through ticket_types with (default None)
    preload_tickets -- whether to load the tickets associated with
                       this TicketType (default False)
    """
    query = db.query(TicketType)

    if id is not None:
        query = query.filter(TicketType.id == id)

    if name is not None:
        query = query.filter(TicketType.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(TicketType.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(TicketType.name).all()


@sys_admin_required
def new(db, actioning_user=None, **kwargs):
    """Create a new TicketType in the database then returns that TicketType.

    The kwargs are parsed such that if a json representation of a
    TicketType is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    name -- the ticket_type name
    """
    new_ticket_type = TicketType(
        name=kwargs['name'],
    )

    db.add(new_ticket_type)
    db.commit()
    return new_ticket_type


@sys_admin_required
def update(db, actioning_user=None, ticket_type=None):
    """Update the given TicketType in the database.

    TicketType must be a TicketType class instance.
    """
    db.add(ticket_type)
    db.commit()


@sys_admin_required
def delete(db, actioning_user=None, ticket_type=None):
    """Remove the given TicketType from the database.

    TicketType must be a TicketType class instance.
    """
    db.delete(ticket_type)
    db.commit()
