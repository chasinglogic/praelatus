"""Blueprint for the user facing half of Praelatus."""

from flask import Blueprint, redirect, request, session

from praelatus.app.ui.forms import RegisterForm
from praelatus.app.ui.helpers import admin_required, auth_required
from praelatus.lib import connection
from praelatus.store import (ProjectStore, TicketStore, TicketTypeStore,
                             UserStore)
from praelatus.templates import render_template

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


@ui.route('/projects/search')
def project_search():
    with connection() as db:
        search = request.args.get('filter')
        if search == '' or search is None:
            search = '*'
        projects = ProjectStore.search(db, search=search,
                                       actioning_user=session.get('user'))
        return render_template('web/projects/search.html', projects=projects)

@ui.route('/<key>')
def show_project(key):
    with connection() as db:
        project = ProjectStore.get(db, uid=key,
                                   actioning_user=session.get('user'))
        if project:
            return render_template('web/projects/show.html', project=project)

        return render_template('web/404.html',
                               message='No project with that key was found.')

@ui.route('/tickets/<project_key>/create', methods=('GET', 'POST'))
def create_ticket(project_key):
    with connection() as db:
        user = session.get('user')
        project = ProjectStore.get(db, actioning_user=user,
                                   uid=project_key)
        if request.method == 'POST':
            new_ticket = request.args
            ticket_type = TicketTypeStore.get(db, name='Bug')
            new_ticket['ticket_type'] = ticket_type
            new_ticket['project'] = project
            if user is None:
                new_ticket['reporter'] = UserStore.get(db, uid='anonymous').jsonify()
            else:
                new_ticket['reporter'] = user
                ticket = TicketStore.new(db, actioning_user=user, **new_ticket)
            return redirect('/%s/%s' % (project.key, ticket.key))
        return render_template('web/tickets/create.html', project=project)


@ui.route('/admin/system')
@admin_required
def admin():
    return render_template('web/admin/sys_info.html')
