from enum import Enum

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class DataTypes(Enum):
    """The valid data types for a Field."""

    FLOAT = 'FLOAT'
    STRING = 'STRING'
    TEXT = 'TEXT'
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

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        """Return name."""
        return self.name


class Field(models.Model):
    """A field is a place to store Data. This describes what kind of data."""

    name = models.CharField(max_length=255, unique=True)
    data_type = models.CharField(max_length=10,
                                 choices=[(x.value, x.value) for x in DataTypes])
    # Only relevant for fields of the OPTION type
    options = models.ManyToManyField(FieldOption, blank=True)

    def is_valid_data_type(self):
        return self.data_type in DataTypes.values()

    def __str__(self):
        """Return name."""
        return self.name


@receiver(pre_save, sender=Field)
def verify_field_data_type(sender, **kwargs):
    if not kwargs['instance'].is_valid_data_type():
        raise InvalidDataTypeException()


class FieldValue(models.Model):
    """An instance of a field with it's value on a some content."""

    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    int_value = models.IntegerField(null=True)
    str_value = models.CharField(max_length=255, null=True)
    flt_value = models.FloatField(null=True)
    date_value = models.DateTimeField(null=True)

    def set_value(self, value):
        """Set the value according to data type. Performs necessary conversion."""
        if self.field.data_type == DataTypes.OPTION.value:
            self.str_value = str(value)
        elif self.field.data_type == DataTypes.STRING.value:
            self.str_value = str(value)
        elif self.field.data_type == DataTypes.FLOAT.value:
            self.flt_value = float(value)
        # TODO: ??????????
        # elif self.field.data_type == DataTypes.DATE.value:
            # self.date_value = (value)
        elif self.field.data_type == DataTypes.INTEGER.value:
            self.int_value = int(value)

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
        if (self.field.data_type == DataTypes.STRING.value or
           self.field.data_type == DataTypes.OPTION.value):
            return self.str_value
        elif self.field.data_type == DataTypes.FLOAT.value:
            return self.flt_value
        elif self.field.data_type == DataTypes.DATE.value:
            return self.date_value
        elif self.field.data_type == DataTypes.INTEGER.value:
            return self.int_value
        else:
            return None

    def __str__(self):
        """Return name."""
        return self.name
