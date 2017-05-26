"""Various helpers and decorators for use in the UI of the app."""

from functools import wraps


def auth_required():
    """Redirect to login page if not authenticated."""
