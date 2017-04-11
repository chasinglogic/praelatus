"""Contains utility functions and decorators for use in lib"""
from functools import wraps


def rollback(fn):
    """rollback is a decorator which on an uncaught exception will
    rollback the db session"""
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            args[0].rollback()
            raise e

    return wrapper
