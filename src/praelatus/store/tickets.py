"""Contains definition for the TicketStore and related classes."""

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
from praelatus.store import Store


class TicketStore(Store):
    """Stores and retrieves tickets."""
    model = Ticket

    @cached
    def get(self, db, uid=None, **kwargs):
        """Get tickets from the database.

        If the keyword arguments id or key are specified returns a single
        sqlalchemy result, otherwise returns all matching results.

        Keyword Arguments
          actioning_user: the user requesting the ticket (default None)
          id: database id (default None)
          uid: the ticket key i.e. TEST-123 (default None)
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

        id = kwargs.pop('id')
        if id is not None:
            query = query.filter(Ticket.id == id)

        if uid is not None:
            query = query.filter(Ticket.key == key)

        result = query.first()
        if result:
            result.transitions = self._get_transitions(db, result)
        return result

    def _get_transitions(self, db, ticket):
        """Get the transitions for the ticket."""
        return db.\
            query(Transition).\
            filter(
                Transition.from_status_id == ticket.status_id,
                Transition.workflow_id == ticket.workflow_id
            ).\
            all()

    def search(self, db, search=None, **kwargs):
        """Search through tickets.

        There are four optional keyword arguments available:
          search: This will filter through tickets based on various
                  fuzzy criteria
          assignee: Get all tickets for assignee, takes a user dict obj.
          reporter: Get all tickets for reporter, takes a user dict obj.
          project_key: Get all tickets for project with project_key.
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

        assignee = kwargs.pop('assignee')
        reporter = kwargs.pop('reporter')
        project_key = kwargs.pop('project_key')

        if assignee is not None:
            query = query.filter(Ticket.assignee_id == assignee['id'])

        if reporter is not None:
            query = query.filter(Ticket.reporter_id == reporter['id'])

        if project_key is not None:
            query = query.filter(Project.key == project_key)

        if search is not None:
            pattern = search.replace('*', '%')
            query = query.filter(
                or_(
                    Ticket.key.like(pattern),
                    Ticket.summary.like('%' + filter + '%'),
                    Label.name.like(pattern),
                    User.username.like(pattern),
                    Status.name.like(pattern)
                )
            )

        return query.order_by(Ticket.key).all()

    def new(self, db, **kwargs):
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
