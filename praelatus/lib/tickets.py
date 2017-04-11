from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from praelatus.models import (Ticket, User, Label, FieldValue, Status,
                              Comment, TicketType)


def get(db, id=None, key=None, reporter=None, assignee=None,
        filter=None, actioning_user=None):
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
