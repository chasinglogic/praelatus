"""Contains utility functions and decorators for use in lib."""

from functools import wraps


def close(fn):
    """Decorate a database function and close the session when finished."""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
        except Exception as e:
            args[0].close()
            raise e
        args[0].close()
        return result
    return wrapper


def rollback(fn):
    """
    Decorate a function and rollback the db on an Exception.

    Requires that the first argument is a sqlalchemy session as
    created by a SessionMaker
    """
    @wraps(fn)
    @close
    def wrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        except Exception as e:
            args[0].rollback()
            raise e
    return wrapper
