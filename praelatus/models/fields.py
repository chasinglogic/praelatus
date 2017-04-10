from base import Base
from sqlalchemy import (Column, DateTime, String, Table,
                        Integer, Float, ForeignKey, relationship)


field_options = Table('field_options', Base.metadata,
                      Column('field_id', Integer,
                             ForeignKey('fields.id')),
                      Column('option_id', Integer,
                             ForeignKey('options.id'))
                      )


class Field(Base):
    __tablename__ = 'fields'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    data_type = Column(String)
    options = relationship('FieldOption', secondary=field_options)


class FieldOption(Base):
    __tablename__ = 'field_options'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class FieldValue(Base):
    __tablename__ = 'field_values'

    ticket_id = Column(Integer, ForeignKey('tickets.id'))
    field_id = Column(Integer, ForeignKey('fields.id'))
    field = relationship('Field')

    int_value = Column(Integer)
    str_value = Column(String(length=255))
    opt_value = Column(String(length=255))
    flt_value = Column(Float)
    date_value = Column(DateTime)
