"""
Contains functions for interacting with labels.

Anywhere a db is taken it is assumed to be a sqlalchemy session
created by a SessionMaker instance.

Anywhere actioning_user is a keyword argument, this is the user
performing the call and the permissions of the provided user will be
checked before committing the action. None is equivalent to an
Anonymous user.
"""

from praelatus.models import Label, Ticket
from sqlalchemy.orm import joinedload


def get(db, id=None, name=None, filter=None,
        actioning_user=None, preload_tickets=False):
    """
    Get labels from the database.

    If the keyword arguments id or name are specified returns a
    single sqlalchemy result, otherwise returns all matching results.

    Keyword Arguments:
    id -- database id (default None)
    name -- the label name (default None)
    filter -- a pattern to search through labels with (default None)
    preload_tickets -- whether to load the tickets associated with
                       this label (default False)
    """
    query = db.query(Label)

    if id is not None:
        query = query.filter(Label.id == id)

    if name is not None:
        query = query.filter(Label.name == name)

    if filter is not None:
        pattern = filter.replace('*', '%')
        query = query.filter(Label.name.like(pattern))

    if preload_tickets:
        query = query.options(joinedload(Ticket))

    if any([id, name]):
        return query.first()
    return query.order_by(Label.name).all()


def new(db, **kwargs):
    """
    Create a new label in the database then returns that label.

    The kwargs are parsed such that if a json representation of a
    label is provided as expanded kwargs it will be handled
    properly.

    If a required argument is not provided then it raises a KeyError
    indicating which key was missing. Useful for returning HTTP 400
    errors.

    Required Keyword Arguments:
    name -- the label name
    """
    new_label = Label(
        name=kwargs['name'],
    )

    db.add(new_label)
    db.commit()
    return new_label


def update(db, actioning_user=None, label=None):
    """
    Update the given label in the database.

    label must be a Label class instance.
    """
    db.add(label)
    db.commit()


def delete(db, actioning_user=None, label=None):
    """
    Remove the given label from the database.

    label must be a Label class instance.
    """
    db.delete(label)
    db.commit()
