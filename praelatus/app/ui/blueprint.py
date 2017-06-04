"""Blueprint for the user facing half of Praelatus."""

from flask import request
from flask import session
from flask import redirect
from flask import Blueprint

from praelatus.lib import connection
from praelatus.store import UserStore
from praelatus.store import TicketStore
from praelatus.store import TicketTypeStore
from praelatus.store import ProjectStore
from praelatus.templates import render_template
from praelatus.models import DuplicateError
from praelatus.app.ui.forms import LoginForm
from praelatus.app.ui.forms import RegisterForm
from praelatus.app.ui.helpers import auth_required
from praelatus.app.ui.forms import CreateTicketForm

ui = Blueprint('ui', __name__)


@ui.route('/')
def index():
    if session.get('user'):
        return redirect('/dashboard')
    return render_template('web/index.html', form=RegisterForm(),
                           action='/register', submit_value='Sign Up')


@ui.route('/dashboard')
@auth_required
def dashboard():
    with connection() as db:
        user = UserStore.get(db, uid=session['user']['username'])
        return render_template('web/dashboard.html', user=user)


@ui.route('/<string:project_key>/<string:ticket_key>')
def show_ticket(project_key, ticket_key):
    with connection() as db:
        project = ProjectStore.get(db, actioning_user=session.get('user'), uid=project_key)
        ticket = TicketStore.get(db, actioning_user=session.get('user'),
                                 project=project, uid=ticket_key)
        return render_template('web/tickets/show.html', ticket=ticket)


@ui.route('/login', methods=('GET', 'POST'))
def login():
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


@ui.route('/register', methods=('GET', 'POST'))
def register():
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


@ui.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


@ui.route('/projects/search')
def project_search():
    with connection() as db:
        search = request.args.get('filter', '*')
        projects = ProjectStore.search(db, search=search,
                                       actioning_user=session.get('user'))
        return render_template('web/projects/search.html', projects=projects)


@ui.route('/users/<username>')
def show_user(username):
    with connection() as db:
        user = UserStore.get(db, uid=username)
        if user:
            return render_template('web/users/show.html', user=user)
        return render_template('web/404.html',
                               message='No user with that username exists.')

@ui.route('/<key>')
def show_project(key):
    with connection() as db:
        project = ProjectStore.get(db, uid=key,
                                   actioning_user=session.get('user'))
        if project:
            return render_template('web/projects/show.html', project=project)

        return render_template('web/404.html',
                               message='No project with that key was found.')

@ui.route('/tickets/create', methods=('GET', 'POST'))
def create_ticket():
    form = CreateTicketForm()
    if form.validate_on_submit():
        user = session.get('user')
        with connection() as db:
            new_ticket = form.data
            project = ProjectStore.get(db, uid=new_ticket.pop('project_name'), actioning_user=user)
            ticket_type = TicketTypeStore.get(db, name=new_ticket.pop('ticket_type'))
            new_ticket['ticket_type'] = ticket_type
            new_ticket['project'] = project
            if user is None:
                new_ticket['reporter'] = UserStore.get(db, uid='anonymous').jsonify()
            else:
                new_ticket['reporter'] = user
            print(new_ticket)
            ticket = TicketStore.new(db, actioning_user=user, **new_ticket)
            return redirect('/%s/%s' % (project.key, ticket.key))
    return render_template('web/tickets/create.html',
                           form=form,
                           action='/tickets/create',
                           submit_value='Create Ticket')
