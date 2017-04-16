"""
Contains functions for interacting with tickets.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from sqlalchemy import or_
from iso8601 import parse_date
from sqlalchemy.orm import joinedload

from praelatus.models import Ticket
from praelatus.models import User
from praelatus.models import Label
from praelatus.models import FieldValue
from praelatus.models import Status
from praelatus.models import Comment
from praelatus.models import TicketType
from praelatus.models.fields import DataTypeError


def get(db, id=None, key=None, reporter=None, assignee=None,
        filter=None, actioning_user=None):
    """
    Get tickets from the database.

    If the keyword arguments id or key are specified returns a single
    sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
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
    """
    Create a new ticket in the database then return that ticket.

    The kwargs are parsed such that if a json representation of a
    ticket is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    project -- json of the project the ticket belongs to
    reporter -- json of the User who the ticket is reported by
    description -- the description for the ticket
    summary -- the summary for the ticket
    ticket_type -- json of the TicketType
    status -- json of the Status
    workflow_id -- the workflow this ticket should be associated with,
                   if not provided it will be determined by the
                   ticket_type and project

    Optional Keyword Arguments:
    assignee -- json of the User who is assigned the ticket
    fields -- an array of json FieldValue's
    labels -- an array of json Labels
    """
    new_ticket = Ticket(
        summary=kwargs['summary'],
        description=kwargs['description'],
        assignee_id=kwargs['assignee']['id'],
        ticket_type_id=kwargs['ticket_type']['id'],
        status_id=kwargs['status']['id'],
        workflow_id=kwargs['workflow_id']
    )

    field_values = kwargs.get('field_values', [])
    for f in field_values:
        field = db.query.filter_by(name=f['name']).first()
        fv = FieldValue(
            field=field
        )
        set_field_value(fv, f['value'])
        new_ticket.fields.append(fv)

    labels = kwargs.get('labels', [])
    for l in labels:
        lbl = Label(name=l['name'])
        new_ticket.labels.append(lbl)

    db.add(new_ticket)
    db.commit()
    return new_ticket


def set_field_value(field_value, val):
    """Set appropriate field_value member based on type of val."""
    if type(val) is int:
        field_value.int_value = val

    elif type(val) is float:
        field_value.flt_value = val

    elif type(val) is str and field_value.field.data_type == 'DATE':
        field_value.date_value = parse_date(val)

    elif type(val) is dict and field_value.field.data_type == 'OPT':
        field_value.opt_value = val['selected']

    elif type(val) is str and field_value.field.data_type == 'STRING':
        field_value.str_value = val

    else:
        raise DataTypeError('no valid data type found')
