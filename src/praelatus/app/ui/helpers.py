"""Various helpers and decorators for use in the UI of the app."""

from flask import url_for
from flask import redirect
from flask import session
from functools import wraps


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('ui.login'))
    return wrapper
