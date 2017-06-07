"""All ui handlers which deal with Users and Sessions."""

from flask import redirect, session

from praelatus.app.ui.blueprint import ui
from praelatus.app.ui.forms import LoginForm, RegisterForm
from praelatus.lib import connection
from praelatus.models import DuplicateError
from praelatus.store import UserStore
from praelatus.templates import render_template


@ui.route('/login', methods=('GET', 'POST'))
def create_session():
    """Create a session for the User."""
    login_form = LoginForm()
    flash = None
    if login_form.validate_on_submit():
        with connection() as db:
            user = UserStore.get(db, uid=login_form.username.data)
            if user is None:
                flash = 'No user with that username.'
            elif UserStore.check_pw(user, login_form.password.data):
                session['user'] = user.jsonify()
                return redirect('/dashboard')
            flash = 'Invalid password.'
    return render_template('web/users/login.html',
                           flash=flash,
                           form=login_form,
                           submit_value='Log In')


@ui.route('/logout')
def delete_session():
    """Delete the users session."""
    session.pop('user', None)
    return redirect('/')


@ui.route('/register', methods=('GET', 'POST'))
def create_user():
    """Create a new user."""
    register_form = RegisterForm()
    flash = None
    if register_form.validate_on_submit():
        try:
            with connection() as db:
                user = UserStore.new(db, **register_form.data)
                session['user'] = user.jsonify()
                # TODO: make a new user screen
                return redirect('/dashboard')
        except DuplicateError:
            flash = 'That username already taken.'
    return render_template('web/users/login.html',
                           flash=flash,
                           action='/register',
                           form=register_form,
                           submit_value='Sign Up')


@ui.route('/users/<username>')
def show_user(username):
    with connection() as db:
        user = UserStore.get(db, uid=username)
        if user:
            return render_template('web/users/show.html', user=user)
        return render_template('web/404.html',
                               message='No user with that username exists.')
