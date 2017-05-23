"""Defines the Ticket, Comment, Label, TickeType, and Status models."""

from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.orm import relationship

from praelatus.models.base import Base


class Ticket(Base):
    """Represents a Ticket in the database."""

    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(),
                          onupdate=datetime.now())
    key = Column(String, unique=True)
    summary = Column(String(length=255))
    description = Column(Text)

    reporter_id = Column(Integer, ForeignKey('users.id'))
    reporter = relationship('User', foreign_keys=reporter_id,
                            backref='reported_tickets', lazy='joined')

    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User', foreign_keys=assignee_id,
                            backref='assigned_tickets', lazy='joined')

    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id'))
    ticket_type = relationship('TicketType', lazy='joined', backref='tickets')

    status_id = Column(Integer, ForeignKey('statuses.id'))
    status = relationship('Status', lazy='joined', backref='tickets')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', lazy='joined', backref='tickets')

    workflow_id = Column(Integer, ForeignKey('workflows.id'))
    workflow = relationship('Workflow', backref='tickets')
    # This should be set by whoever is retrieving the ticket
    transitions = []

    comments = relationship('Comment', backref='ticket')

    fields = relationship('FieldValue', backref='field_values',
                          lazy='joined')

    def jsonify(self):
        """Override BaseModel jsonify."""
        jsn = {
            'id': self.id,
            'key': self.key,
            'summary': self.summary,
            'description': self.description,
            'ticket_type': self.ticket_type.jsonify(),
            'status': self.status.jsonify(),
            'project': self.project.jsonify(),
            'reporter': self.reporter.jsonify(),
            'workflow_id': self.workflow_id,
            'created_date': str(self.created_date),
            'updated_date': str(self.updated_date),
            'transitions': [x.jsonify() for x in self.transitions],
            'fields': [x.jsonify() for x in self.fields],
            'labels': [x.name for x in self.labels]
        }

        if self.assignee and isinstance(self.assignee, Base):
            jsn['assignee'] = self.assignee.jsonify()

        return jsn


class Comment(Base):
    """Represents a Comment on a Ticket in the database."""

    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(),
                          onupdate=datetime.now())
    body = Column(Text)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', foreign_keys=author_id)

    ticket_id = Column(Integer, ForeignKey('tickets.id'))

    def jsonify(self):
        """Override BaseModel jsonify."""
        return {
            'id': self.id,
            'author': self.author.jsonify(),
            'ticket_key': self.ticket.key,
            'updated_date': str(self.updated_date),
            'created_date': str(self.created_date),
            'body': self.body
        }


# A many to many table for connecting the Label and Ticket classes
labels_tickets = Table('labels_tickets', Base.metadata,
                       Column('ticket_id', Integer,
                              ForeignKey('tickets.id')),
                       Column('label_id', Integer,
                              ForeignKey('labels.id'))
                       )


class Label(Base):
    """Represents a Label in the database."""

    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tickets = relationship('Ticket', secondary=labels_tickets,
                           backref='labels')


class TicketType(Base):
    """Represents a TicketType in the database."""

    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)


class Status(Base):
    """Represents a Status in the database."""

    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
