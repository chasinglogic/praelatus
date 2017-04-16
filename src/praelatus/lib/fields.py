"""
Contains functions for interacting with fields.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from praelatus.models import Field
from praelatus.models import FieldOption
from praelatus.models.fields import DATA_TYPES
from praelatus.lib.utils import rollback


def get(db, id=None, name=None, filter=None):
    """
    Get fields from the database.

    If the keyword arguments id or name are specified returns a single
    sqlalchemy result, otherwise returns all matching results.

    keyword arguments:
    actioning_user -- the user requesting the field (default None)
    id -- database id (default None)
    name -- the field name (default None)
    filter -- a pattern to search through fields with (default None)
    """
    query = db.query(Field)

    if id is not None:
        query = query.filter(Field.id == id)

    if name is not None:
        query = query.filter(Field.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Field.name.like(pattern))

    if any([id, name]):
        return query.first()
    return query.order_by(Field.name).all()


def valid_type(data_type):
    """Raise an exception if data_type isn't in the accepted DATA_TYPES."""
    if data_type in DATA_TYPES:
        return data_type
    raise Exception('Invalid data type %s please select from %s' %
                    (data_type, DATA_TYPES))


@rollback
def new(db, **kwargs):
    """
    Create a new field in the database then returns that field.

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
        data_type=valid_type(kwargs['data_type']),
    )

    options = kwargs.get('options', [])
    for o in options:
        new_field.options.append(FieldOption(name=o))

    db.add(new_field)
    db.commit()
    return new_field


@rollback
def update(db, field):
    """
    Update the given field in the database.

    field must be a Field class instance.
    """
    db.add(field)
    db.commit()
    return field


@rollback
def delete(db, field):
    """
    Remove the given field from the database.

    field must be a Field class instance.
    """
    db.delete(field)
    db.commit()
