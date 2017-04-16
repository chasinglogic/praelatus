"""Contains definitions for the Field and related models."""

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import Integer
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from praelatus.models.base import Base

# Consider using an Enum here?
DATA_TYPES = [
    'FLOAT',
    'STRING',
    'INT',
    'DATE',
    'OPT'
]

field_options = Table('fields_options', Base.metadata,
                      Column('field_id', Integer,
                             ForeignKey('fields.id')),
                      Column('option_id', Integer,
                             ForeignKey('field_options.id'))
                      )


class Field(Base):
    """Represents a Field in the database."""

    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    data_type = Column(String)
    options = relationship('FieldOption', secondary=field_options)


class FieldOption(Base):
    """For Fields with the data_type OPT stores those options."""

    __tablename__ = 'field_options'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class FieldValue(Base):
    """Store an instance of a Field's value on a Ticket."""

    __tablename__ = 'field_values'
    __table_args__ = (
        UniqueConstraint('field_id', 'ticket_id'),
    )

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    field_id = Column(Integer, ForeignKey('fields.id'))
    field = relationship('Field')

    int_value = Column(Integer)
    str_value = Column(String(length=255))
    opt_value = Column(String(length=255))
    flt_value = Column(Float)
    date_value = Column(DateTime)


class DataTypeError(Exception):
    """A simple Exception which indicates an invalid DataType for a field."""

    pass
