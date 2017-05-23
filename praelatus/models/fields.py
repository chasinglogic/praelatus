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
from enum import Enum

from praelatus.models.base import Base


class DATA_TYPES(Enum):
    """The valid data types for a Field."""

    FLOAT = 'FLOAT'
    STRING = 'STRING'
    INT = 'INT'
    DATE = 'DATE'
    OPT = 'OPT'

    @staticmethod
    def values():
        """Return a list of the valid DATA_TYPES as strings."""
        vals = []
        for typ in DATA_TYPES:
            vals.append(typ.value)
        return vals

    def __repr__(self):
        """Call self.__str__."""
        return self.__str__

    def __str__(self):
        """Return a string friendly printing of the DATA_TYPES."""
        return "[ %s, %s, %s, %s, %s ]" %\
            (self.FLOAT, self.STRING, self.INT, self.DATE, self.OPT)


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
    options = relationship('FieldOption', secondary=field_options,
                           lazy='subquery')

    def jsonify(self):
        """Override BaseModel jsonify."""
        jsn = {
            'id': self.id,
            'name': self.name,
            'data_type': self.data_type
        }

        if self.data_type == 'OPT':
            jsn['options'] = [opt.name for opt in self.options]

        return jsn


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

    def jsonify(self):
        """Override BaseModel jsonify."""
        # Jsn['Value'] = the appropriate value, based on field data type.
        jsn = {
            'id': self.id,
            'name': self.field.name,
            'data_type': self.field.data_type
        }

        if self.field.data_type == 'OPT':
            jsn['value'] = self.opt_value
            jsn['options'] = []
            for opt in self.field.options:
                jsn['options'].append(opt.name)
        elif self.field.data_type == 'STRING':
            jsn['value'] = self.str_value
        elif self.field.data_type == 'FLOAT':
            jsn['value'] = self.flt_value
        elif self.field.data_type == 'DATE':
            jsn['value'] = str(self.date_value)
        elif self.field.data_type == 'INT':
            jsn['value'] = self.int_value

        return jsn


class DataTypeError(Exception):
    """A simple Exception which indicates an invalid DataType for a field."""

    pass
