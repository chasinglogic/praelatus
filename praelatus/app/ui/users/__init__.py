"""All ui handlers which deal with Users and Sessions."""

from flask import redirect, session, request

from praelatus.app.ui.blueprint import ui
from praelatus.app.ui.forms import LoginForm, RegisterForm
from praelatus.app.ui.helpers import auth_required
from praelatus.lib import connection
from praelatus.models import DuplicateError
from praelatus.store import UserStore
from praelatus.templates import render_template


@ui.route('/login', methods=('GET', 'POST'))
def login():
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
                return redirect(request.args.get('destination', '/dashboard'))
            flash = 'Invalid password.'
    return render_template('users/login.html',
                           flash=flash,
                           form=login_form,
                           submit_value='Log In')


@ui.route('/logout')
def logout():
    """Delete the users session."""
    session.pop('user', None)
    return redirect('/')


@ui.route('/register', methods=('GET', 'POST'))
def register():
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
    return render_template('users/login.html',
                           flash=flash,
                           action='/register',
                           form=register_form,
                           submit_value='Sign Up')


@ui.route('/users/<username>')
def show_user(username):
    """Show a user's profile page."""
    with connection() as db:
        user = UserStore.get(db, uid=username)
        if user:
            return render_template('users/show.html', user=user)
        return render_template('404.html',
                               message='No user with that username exists.')


@ui.route('/dashboard')
@auth_required
def dashboard():
    """Show the logged in user's dashboard."""
    with connection() as db:
        user = UserStore.get(db, uid=session['user']['username'])
        return render_template('dashboard/index.html', user=user)
