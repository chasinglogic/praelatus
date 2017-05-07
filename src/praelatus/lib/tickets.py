"""Contains functions for interacting with tickets.

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
from praelatus.models import Field
from praelatus.models import FieldValue
from praelatus.models import Status
from praelatus.models import Comment
from praelatus.models import Project
from praelatus.models import Transition
from praelatus.models.fields import DataTypeError
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import add_permission_query
from praelatus.lib.permissions import has_permission
from praelatus.lib.permissions import is_system_admin
from praelatus.lib.redis import cached


@cached
def get(db, id=None, key=None, reporter=None, assignee=None, project_key=None,
        filter=None, actioning_user=None, preload_comments=False, cached=None):
    """Get tickets from the database.

    If the keyword arguments id or key are specified returns a single
    sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    actioning_user -- the user requesting the ticket (default None)
    id: database id (default None)
    key: the ticket key i.e. TEST-123 (default None)
    reporter: User class instance who is the reporter (default None)
    assignee: User class instance who is the assignee (default None)
    filter: a pattern to search through tickets with (default None)
    """
    query = db.query(Ticket).options(
        joinedload(Ticket.ticket_type),
        joinedload(Ticket.status),
        joinedload(Ticket.fields).
        joinedload(FieldValue.field).
        joinedload(Field.options),
        joinedload(Ticket.labels),
        joinedload(Ticket.assignee),
        joinedload(Ticket.reporter)
    ).join(
        Project
    )

    query = add_permission_query(db, query, actioning_user, 'VIEW_PROJECT')

    if id is not None:
        query = query.filter(Ticket.id == id)

    if key is not None:
        query = query.filter(Ticket.key == key)

    if assignee is not None:
        query = query.filter(Ticket.assignee_id == assignee['id'])

    if reporter is not None:
        query = query.filter(Ticket.reporter_id == reporter['id'])

    if project_key is not None:
        query = query.filter(Project.key == project_key)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(
            or_(
                Ticket.key.like(pattern),
                Ticket.summary.like('%' + filter + '%'),
                Label.name.like(pattern),
                User.username.like(pattern),
                Status.name.like(pattern)
            )
        )

    if any([id, key]):
        result = query.first()
        if result:
            result.transitions = _get_transitions(db, result)
        return result
    return query.order_by(Ticket.key).all()


def _get_transitions(db, ticket):
    """Get the transitions for the ticket."""
    return db.\
        query(Transition).\
        filter(
            Transition.from_status_id == ticket.status_id,
            Transition.workflow_id == ticket.workflow_id
        ).\
        all()


def new(db, **kwargs):
    """Create a new ticket in the database then return that ticket.

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
        reporter_id=kwargs['reporter']['id'],
        ticket_type_id=kwargs['ticket_type']['id'],
        project_id=kwargs['project']['id'],
    )

    # Raw sql here is clearer and faster than using orm
    new_ticket.workflow_id = db.execute(
        "select w.id from workflows as w "
        "join workflows_projects as wkp on wkp.workflow_id = w.id"
        " where wkp.project_id = :pid",
        {"pid": new_ticket.project_id}).\
        first()[0]

    new_ticket.status_id = db.query(Transition.to_status_id).filter(
        Transition.workflow_id == new_ticket.workflow_id,
        Transition.name == 'Create'
    ).first()

    count = db.query(Ticket.id).\
        filter(Ticket.project_id == kwargs['project']['id']).count()
    new_ticket.key = kwargs['project']['key'] + '-' + str(count + 1)

    assignee = kwargs.get('assignee')
    if assignee is not None:
        new_ticket.assignee_id = assignee['id']

    field_values = kwargs.get('fields', [])
    for f in field_values:
        field = db.query(Field).filter_by(name=f['name']).first()
        if field is None:
            raise KeyError('no field with name ' + f['name'] + ' found')
        fv = FieldValue(
            field=field
        )
        set_field_value(fv, f['value'])
        new_ticket.fields.append(fv)
        db.add(fv)
        db.commit()

    labels = kwargs.get('labels', [])
    for l in labels:
        lbl = db.query(Label).filter_by(name=l).first()
        if lbl is None:
            lbl = Label(name=l)
            db.add(lbl)
            db.commit()
        new_ticket.labels.append(lbl)

    db.add(new_ticket)
    db.commit()
    return new_ticket


@permission_required('EDIT_TICKET')
def update(db, actioning_user=None, project=None,
           orig_ticket=None, ticket=None):
    """Update the given ticket in the database.

    ticket must be a Ticket class instance or a JSON ticket object. If
    it is JSON then orig_ticket must be supplied which is the Ticket
    class instance that's being updated.
    """
    if isinstance(ticket, Ticket):
        db.add(ticket)
        return

    orig_ticket.summary = ticket['summary']
    orig_ticket.description = ticket['description']
    orig_ticket.reporter_id = ticket['reporter']['id']

    if ticket.get('assignee') is not None:
        orig_ticket.assignee_id = ticket['assignee']['id']

    field_values = ticket.get('fields', [])
    new_fields = []
    for f in field_values:
        fv = db.query(FieldValue).filter_by(id=f.get('id', 0)).first()
        if fv is None:
            field = db.query(Field).filter_by(name=f['name']).first()
            if field is None:
                raise KeyError('no field with name ' + f['name'] + ' found')
            fv = FieldValue(
                field=field
            )

        set_field_value(fv, f['value'])
        db.add(fv)
        new_fields.append(fv)
        db.commit()

    orig_ticket.fields = new_fields

    labels = ticket.get('labels', [])
    if orig_ticket.labels != labels:
        new_labels = []
        for l in labels:
            lbl = db.query(Label).filter_by(name=l).first()
            if lbl is None:
                lbl = Label(name=l)
                db.add(lbl)
                db.commit()
            new_labels.append(lbl)

        orig_ticket.labels = new_labels

    db.add(orig_ticket)
    db.commit()


@permission_required('REMOVE_TICKET')
def delete(db, actioning_user=None, project=None, ticket=None):
    """Remove the given ticket in the database.

    ticket must be a Ticket class instance.
    """
    db.delete(ticket)
    db.commit()


@permission_required('COMMENT_TICKET')
def add_comment(db, actioning_user=None, project=None, **kwargs):
    """Add comment to if acitoning_user has permission.

    Required Keyword Arguments:
    actioning_user -- user who is making the comment
    author -- json representation of a User who is the author
    project -- the project the ticket belongs to
    ticket_id -- the id of the ticket the comment is being added to
    """
    new_comment = Comment(author_id=kwargs['author']['id'],
                          body=kwargs['body'],
                          ticket_id=kwargs['ticket_id'])
    db.add(new_comment)
    db.commit()
    return new_comment


@permission_required('VIEW_PROJECT')
def get_comments(db, ticket_id=0, ticket_key=None,
                 actioning_user=None, project=None):
    """Get all comments for the given ticket_id or ticket_key."""
    query = db.query(Comment)
    if ticket_key:
        query = query.join(Ticket).filter(Ticket.key == ticket_key)
    else:
        query = query.filter(Comment.ticket_id == ticket_id)

    return query.all()


@permission_required('VIEW_PROJECT')
def get_comment(db, comment_id, actioning_user=None, project=None):
    """Get a single comment by ID."""
    return db.query(Comment).filter_by(id=comment_id).first()


def update_comment(db, comment, actioning_user=None, project=None):
    """Update the given comment.

    comment must be an instance of the Comment class.

    Not using permission_required to make as little DB calls as needed.
    """
    if (
        is_system_admin(db, actioning_user) or

        has_permission(db, 'EDIT_COMMENT', project, actioning_user) or

        (comment.author_id == actioning_user['id'] and
         has_permission(db, 'EDIT_OWN_COMMENT', project, actioning_user))
    ):
        db.add(comment)
        db.commit()
        return

    raise PermissionError('permission denied')


def delete_comment(db, comment, actioning_user, project):
    """Delete the given comment.

    comment must be an instance of the Comment class.

    Not using permission_required to make as little DB calls as needed.
    """
    if (
        is_system_admin(db, actioning_user) or

        has_permission(db, 'EDIT_COMMENT', project, actioning_user) or

        (comment.author_id == actioning_user['id'] and
         has_permission(db, 'EDIT_OWN_COMMENT', project, actioning_user))
    ):
        db.delete(comment)
        db.commit()
        return

    raise PermissionError('permission denied')


def set_field_value(field_value, val):
    """Set appropriate field_value member based on type of val."""
    if type(val) is int:
        field_value.int_value = val

    elif type(val) is float:
        field_value.flt_value = val

    elif type(val) is str and field_value.field.data_type == 'DATE':
        field_value.date_value = parse_date(val)

    elif type(val) is str and field_value.field.data_type == 'OPT':
        field_value.opt_value = val

    elif type(val) is str and field_value.field.data_type == 'STRING':
        field_value.str_value = val

    else:
        raise DataTypeError('no valid data type found')
