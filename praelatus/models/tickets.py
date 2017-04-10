from praelatus.models.base import Base
from datetime import datetime
from sqlalchemy import (Column, DateTime, String, Table, Text,
                        Integer, ForeignKey)
from sqlalchemy.orm import relationship


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(),
                          onupdate=datetime.now())
    key = Column(String)
    summary = Column(String(length=255))
    description = Column(Text)

    reporter_id = Column(Integer, ForeignKey('users.id'))
    reporter = relationship('User', foreign_keys=reporter_id,
                            backref='reported_tickets')

    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User', foreign_keys=assignee_id,
                            backref='assigned_tickets')

    ticket_type_id = Column(Integer, ForeignKey('ticket_types.id'))
    ticket_type = relationship('TicketType')

    status_id = Column(Integer, ForeignKey('statuses.id'))
    status = relationship('Status')

    workflow_id = Column(Integer, ForeignKey('workflows.id'))

    comments = relationship('Comment', backref='comments')
    fields = relationship('FieldValue', backref='field_values')


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now(),
                          onupdate=datetime.now())
    body = Column(Text)

    author_id = Column(Integer, ForeignKey('users.id'))
    author = relationship('User', foreign_keys=author_id)

    ticket_id = Column(Integer, ForeignKey('tickets.id'))


labels_tickets = Table('labels_tickets', Base.metadata,
                       Column('ticket_id', Integer,
                              ForeignKey('tickets.id')),
                       Column('label_id', Integer,
                              ForeignKey('labels.id'))
                       )


class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    tickets = relationship('Ticket', secondary=labels_tickets,
                           backref='labels')


class TicketType(Base):
    __tablename__ = 'ticket_types'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True)
    name = Column(String)
