from enum import Enum

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from tickets.models import Ticket


class DataTypes(Enum):
    """The valid data types for a Field."""

    FLOAT = 'FLOAT'
    STRING = 'STRING'
    INTEGER = 'INTEGER'
    DATE = 'DATE'
    OPTION = 'OPTION'

    @classmethod
    def values(cls):
        return [x.value for x in cls]

    def __repr__(self):
        """Call self.__str__."""
        return self.__str__

    def __str__(self):
        """Return a string friendly printing of the DATA_TYPES."""
        return "[ %s, %s, %s, %s, %s ]" %\
            (self.FLOAT.value, self.STRING.value, self.INT.value,
             self.DATE.value, self.OPT)


class InvalidDataTypeException(Exception):
    """Raised when a failed is saved with an invalid data type."""
    pass


class FieldOption(models.Model):
    """An option in a select type field."""

    name = models.CharField(max_length=255)


class Field(models.Model):
    """A field is a place to store Data. This describes what kind of data."""

    name = models.CharField(max_length=255, unique=True)
    data_type = models.CharField(max_length=10)
    options = models.ManyToManyField(FieldOption)

    def is_valid_data_type(self):
        return self.data_type in DataTypes.values()


@receiver(pre_save, sender=Field)
def verify_field_data_type(sender, **kwargs):
    if not kwargs['instance'].is_valid_data_type():
        raise InvalidDataTypeException()


class FieldValue(models.Model):
    """An instance of a field with it's value on a ticket."""

    field = models.ForeignKey(Field)
    ticket = models.ForeignKey(Ticket, related_name='fields')

    int_value = models.IntegerField(null=True)
    str_value = models.CharField(max_length=255, null=True)
    opt_value = models.CharField(max_length=255, null=True)
    flt_value = models.FloatField(null=True)
    date_value = models.DateTimeField(null=True)

    @property
    def name(self):
        return self.field.name

    @property
    def data_type(self):
        return self.field.data_type

    @property
    def options(self):
        if len(self.field.options.all()) == 0:
            return None
        return self.field.options

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
            return self.date_value
        elif self.field.data_type == DataTypes.INTEGER.value:
            return self.int_value
        else:
            return None
