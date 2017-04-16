"""Contains utility functions and decorators for use in lib."""

from functools import wraps


def rollback(fn):
    """
    Decorate a function and rollback the db on an Exception.

    Requires that the first argument is a sqlalchemy session as
    created by a SessionMaker
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            args[0].rollback()
            raise e

    return wrapper
