"""Contains definition for the FieldStore class.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from praelatus.store import Store
from praelatus.models import Field
from praelatus.models.fields import FieldOption
from praelatus.models.fields import DATA_TYPES
from praelatus.lib.permissions import sys_admin_required


class FieldStore(Store):
    """Stores and retrieves workflows."""

    @sys_admin_required
    def new(self, db, actioning_user=None, **kwargs):
        """Create a new field in the database then returns that field.

        The kwargs are parsed such that if a json representation of a
        field is provided as expanded kwargs it will be handled
        properly.

        If a required argument is not provided then it raises a KeyError
        indicating which key was missing. Useful for returning HTTP 400
        errors.

        Required Keyword Arguments:
        name -- the field name
        data_type -- the field's data_type as specified by DATA_TYPES

        Optional Keyword Arguments:
        options -- an array of json FieldOptions required if DATA_TYPE == 'OPT'
        """
        new_field = Field(
            name=kwargs['name'],
            data_type=self.valid_type(kwargs['data_type'])
        )

        options = kwargs.get('options', [])
        for o in options:
            res = db.query(FieldOption).\
                filter_by(name=o).\
                first()
            if res is not None:
                new_field.options.append(res)
            else:
                new_field.options.append(FieldOption(name=o))

        db.add(new_field)
        db.commit()

        return new_field

    @staticmethod
    def valid_type(data_type):
        """Raise an exception if data_type isn't in the accepted DATA_TYPES."""
        if data_type in DATA_TYPES.values():
            return data_type
        raise Exception('Invalid data type %s please select from %s' %
                        (data_type, DATA_TYPES.values()))


store = FieldStore(Field)
