from enum import Enum
from tickets.models import Ticket
from django.db import models


class DataTypes(Enum):
    """The valid data types for a Field."""

    FLOAT = 'FLOAT'
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    DATE = 'DATE'
    OPTION = 'OPTION'

    def __repr__(self):
        """Call self.__str__."""
        return self.__str__

    def __str__(self):
        """Return a string friendly printing of the DATA_TYPES."""
        return "[ %s, %s, %s, %s, %s ]" %\
            (self.FLOAT, self.STRING, self.INT, self.DATE, self.OPT)


class FieldOption(models.Model):
    """An option in a select type field."""

    name = models.CharField(max_length=255)


class Field(models.Model):
    """A field is a place to store Data. This describes what kind of data."""

    name = models.CharField(max_length=255, unique=True)
    data_type = models.CharField(max_length=10)
    options = models.ManyToManyField(FieldOption)


class FieldValue(models.Model):
    """An instance of a field with it's value on a ticket."""

    field = models.ForeignKey(Field)
    ticket = models.ForeignKey(Ticket, related_name='fields')

    int_value = models.IntegerField()
    str_value = models.CharField(max_length=255)
    opt_value = models.CharField(max_length=255)
    flt_value = models.FloatField()
    date_value = models.DateTimeField()

    @property
    def value(self):
        """Return the value of this FieldValue based on data type."""
        if self.field.data_type == DataTypes.OPTION.value:
            return self.opt_value
        elif self.field.data_type == DataTypes.STRING.value:
            return self.str_value
        elif self.field.data_type == DataTypes.FLOAT.value:
            return self.flt_value
        elif self.field.data_type == DataTypes.DATE.value:
            return str(self.date_value)
        elif self.field.data_type == DataTypes.INTEGER.value:
            return self.int_value
        else:
            return None
