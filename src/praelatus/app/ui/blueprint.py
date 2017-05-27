"""Blueprint for the user facing half of Praelatus."""

import praelatus.lib.tokens as tokens

from flask import redirect
from flask import Blueprint
from flask import g

from praelatus.lib import connection
from praelatus.store import UserStore
from praelatus.store import TicketStore
from praelatus.store import ProjectStore
from praelatus.templates import render_template
from praelatus.app.ui.forms.login import LoginForm

ui = Blueprint('ui', __name__)

@ui.route('/')
def index():
    return render_template('web/index.html')


@ui.route('/<string:project_key>/<string:ticket_key>')
def show_ticket(project_key, ticket_key):
    with connection() as db:
        project = ProjectStore.get(db, actioning_user=g.user, uid=project_key)
        ticket = TicketStore.get(db, actioning_user=g.user,
                                 project=project, uid=ticket_key
        )
        return render_template('web/tickets/show.html', ticket=ticket)


@ui.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        with connection() as db:
            user = UserStore.get(db, uid=form.username.data)
            if user is None:
                return render_template('web/users/login.html',
                                       flash='No user with that username.')
            if UserStore.check_pw(user, form.password.data):
                resp = redirect('/')
                session = tokens.gen_session_id(user.jsonify())
                resp.set_cookie('PRAE_SESSION', session)
                return resp
            return render_template('web/users/login.html', flash='Invalid Password')
    return render_template('web/users/login.html', form=form)
