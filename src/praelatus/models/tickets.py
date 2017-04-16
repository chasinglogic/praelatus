"""Defines the Ticket, Comment, Label, TickeType, and Status models."""

from praelatus.models.base import Base
from datetime import datetime
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


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
    ticket_type = relationship('TicketType', lazy='joined')

    status_id = Column(Integer, ForeignKey('statuses.id'))
    status = relationship('Status', lazy='joined')

    project_id = Column(Integer, ForeignKey('projects.id'))
    project = relationship('Project', lazy='joined')

    workflow_id = Column(Integer, ForeignKey('workflows.id'))

    comments = relationship('Comment', backref='ticket',
                            lazy='joined')

    fields = relationship('FieldValue', backref='field_values',
                          lazy='joined')


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
