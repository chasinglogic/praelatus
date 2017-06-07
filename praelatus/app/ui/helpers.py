"""Various helpers and decorators for use in the UI of the app."""

from functools import wraps

from flask import redirect, session, url_for

from praelatus.templates import render_template


def auth_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if session.get('user'):
            return fn(*args, **kwargs)
        else:
            return redirect(url_for('ui.login'))
    return wrapper


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user = session.get('user')
        if user and user.get('is_admin'):
            return fn(*args, **kwargs)
        else:
            return render_template('404.html',
                                   message='You must be an Admin to access that screen.')
    return wrapper
