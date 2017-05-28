"""Blueprint for the user facing half of Praelatus."""

from flask import request
from flask import session
from flask import redirect
from flask import Blueprint

from praelatus.lib import connection
from praelatus.store import UserStore
from praelatus.store import TicketStore
from praelatus.store import ProjectStore
from praelatus.templates import render_template
from praelatus.app.ui.forms.login import LoginForm

ui = Blueprint('ui', __name__)


@ui.route('/')
def index():
    return render_template('web/index.html', login_form=LoginForm())


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
    if login_form.validate_on_submit():
        with connection() as db:
            user = UserStore.get(db, uid=login_form.username.data)
            if user is None:
                return render_template('web/users/login.html',
                                       flash='No user with that username.')
            if UserStore.check_pw(user, login_form.password.data):
                session['user'] = user.jsonify()
                return redirect('/')
            return render_template('web/users/login.html', flash='Invalid Password')
    return render_template('web/users/login.html',
                           login_form=login_form,
                           register_form=None)


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
