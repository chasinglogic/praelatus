from base import Base

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.now())
    updated_date = Column(DateTime, default=datetime.now())
    key = Column(String)
    summary = Column(String)
    description = Column(String)

    reporter_id = Column(Integer, ForeignKey('users.id'))
    reporter = relationship('User')

    assignee_id = Column(Integer, ForeignKey('users.id'))
    assignee = relationship('User')

    type_id = Column(Integer, ForeignKey('ticket_types.id'))
    type = relationship('TicketType')

    status_id = Column(Integer, ForeignKey('statuses.id'))
    status = relationship('Status')

    workflow_id = Column(Integer, ForeignKey('workflows.id'))

    comments = relationship('Comment', backref='comments')
    fields = relationship('FieldValue', backref='field_values')


