"""
Contains methods for interacting with tickets.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from praelatus.models import Ticket
from praelatus.models import User
from praelatus.models import Label
from praelatus.models import FieldValue
from praelatus.models import Status
from praelatus.models import Comment
from praelatus.models import TicketType


def get(db, id=None, key=None, reporter=None, assignee=None,
        filter=None, actioning_user=None):
    """
    Get a ticket from the database.

    If the keyword arguments id or key are specified returns a single
    sqlalchemy result, otherwise returns all matching results.

    keyword arguments:
    actioning_user -- the user requesting the ticket (default None)
    id -- database id (default None)
    key -- the ticket key i.e. TEST-123 (default None)
    reporter -- User class instance who is the reporter (default None)
    assignee -- User class instance who is the assignee (default None)
    filter -- a pattern to search through tickets with (default None)
    """

    query = db.query(Ticket).join(
        FieldValue,
        Label,
        Status,
        Comment,
        TicketType
    ).options(
        joinedload(Ticket.assignee),
        joinedload(Ticket.reporter)
    )

    if id is not None:
        query = query.filter(Ticket.id == id)

    if key is not None:
        query = query.filter(Ticket.key == key)

    if assignee is not None:
        query = query.filter(Ticket.assignee == assignee)

    if reporter is not None:
        query = query.filter(Ticket.reporter == reporter)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(
            or_(
                Ticket.key.like(pattern),
                Ticket.summary.like('%'+filter+'%'),
                Label.name.like(pattern),
                User.username.like(pattern),
                Status.name.like(pattern)
            )
        )

    if any([id, key]):
        return query.first()
    return query.order_by(Ticket.key).all()


def new(db, **kwargs):
