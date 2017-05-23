"""Contains definition for the TicketStore.

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
from praelatus.models import Project
from praelatus.models import Transition
from praelatus.models.fields import DataTypeError
from praelatus.lib.permissions import permission_required
from praelatus.lib.permissions import add_permission_query
from praelatus.lib.redis import cached
from praelatus.store import Store


class TicketStore(Store):
    """Stores and retrieves tickets."""

    @cached
    def get(self, db, uid=None, actioning_user=None, **kwargs):
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

        uid = kwargs.pop('id', uid)

        if type(uid) is int:
            query = query.filter(Ticket.id == uid)
        elif type(uid) is str:
            query = query.filter(Ticket.key == uid)
        else:
            return None

        result = query.first()
        if result:
            result.transitions = self._get_transitions(db, result)
        return result

    def _get_transitions(self, db, ticket):
        """Get the transitions for the ticket."""
        return db.query(Transition).filter(
            Transition.from_status_id == ticket.status_id,
            Transition.workflow_id == ticket.workflow_id
        ).all()

    def search(self, db, search=None, actioning_user=None, **kwargs):
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

        assignee = kwargs.pop('assignee', None)
        reporter = kwargs.pop('reporter', None)
        project_key = kwargs.pop('project_key', None)

        if assignee is not None:
            query = query.filter(Ticket.assignee_id == assignee['id'])
        elif reporter is not None:
            query = query.filter(Ticket.reporter_id == reporter['id'])
        elif project_key is not None:
            query = query.filter(Project.key == project_key)
        elif search is not None:
            pattern = search.replace('*', '%')
            query = query.filter(
                or_(
                    Ticket.key.like(pattern),
                    Ticket.summary.like('%' + search + '%'),
                    Label.name.like(pattern),
                    User.username.like(pattern),
                    Status.name.like(pattern)
                )
            )
        else:
            return None

        return query.order_by(Ticket.key).all()

    @permission_required('CREATE_TICKET')
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

        new_ticket.status_id = self._get_transition(db, new_ticket, 'Create')
        new_ticket.key = self.get_next_ticket_key(db, kwargs['project'])

        assignee = kwargs.get('assignee')
        if assignee is not None:
            new_ticket.assignee_id = assignee['id']

        field_values = kwargs.get('fields', [])
        new_ticket.fields = self.parse_field_values(db, field_values)
        labels = kwargs.get('labels', [])
        new_ticket.labels = self.parse_labels(db, labels)
        db.add(new_ticket)
        db.commit()
        return new_ticket

    @permission_required('TRANSITION_TICKET')
    def transition_ticket(self, db, ticket, transition_name):
        """Perform transition on ticket indicated by transition_name."""
        transition = self._get_transition(db, ticket, transition_name)
        if transition is None:
            raise KeyError('Not a valid transition.')
        ticket.status_id = transition.to_status_id
        db.add(ticket)
        db.commit()
        return (transition, ticket)

    def _get_transition(self, db, ticket, transition_name):
        """Find the transition and return the new status_id for the ticket."""
        query = db.query(Transition.to_status_id).filter(
            Transition.workflow_id == ticket.workflow_id,
            Transition.name == 'Create'
        )

        if transition_name != 'Create':
            query = query.\
                filter(Transition.from_status_id == ticket.status_id)
        return query.first()

    def get_next_ticket_key(self, db, project):
        """Return the appropriate ticket key."""
        count = db.query(Ticket.id).\
            filter(Ticket.project_id == project['id']).count()
        return '{}-{}'.format(project['key'], count + 1)

    @permission_required('EDIT_TICKET')
    def update(self, db, model=None, orig_ticket=None, **kwargs):
        """Update the given ticket in the database.

        model must be a Ticket class instance or a JSON ticket object. If
        it is JSON then orig_ticket must be supplied which is the Ticket
        class instance that's being updated.
        """
        if isinstance(model, Ticket):
            db.add(model)
            return

        orig_ticket.summary = model['summary']
        orig_ticket.description = model['description']
        orig_ticket.reporter_id = model['reporter']['id']

        if model.get('assignee') is not None:
            orig_ticket.assignee_id = model['assignee']['id']

        field_values = model.get('fields', [])
        orig_ticket.fields = self.parse_field_values(db, field_values)

        labels = model.get('labels', [])
        if orig_ticket.labels != labels:
            orig_ticket.labels = self.parse_labels(db, labels)

        db.add(orig_ticket)
        db.commit()

    def parse_labels(self, db, labels):
        """Convert JSON Labels to Label objects."""
        new_labels = []
        for l in labels:
            lbl = db.query(Label).filter_by(name=l).first()
            if lbl is None:
                lbl = Label(name=l)
                db.add(lbl)
                db.commit()
            new_labels.append(lbl)
        return new_labels

    def parse_field_values(self, db, field_values):
        """Convert JSON Field Values to FieldValue objects."""
        new_fields = []
        for f in field_values:
            fv = db.query(FieldValue).filter_by(id=f.get('id', 0)).first()
            if fv is None:
                field = db.query(Field).filter_by(name=f['name']).first()
                if field is None:
                    raise KeyError('no field with name %s found' % f['name'])
                fv = FieldValue(
                    field=field
                )

            self.set_field_value(fv, f['value'])
            db.add(fv)
            db.commit()
            new_fields.append(fv)
        return new_fields

    @permission_required('REMOVE_TICKET')
    def delete(self, db, model=None, **kwargs):
        """Remove the given ticket from the database."""
        db.delete(model)
        db.commit()

    def set_field_value(self, field_value, val):
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


store = TicketStore(Ticket)
