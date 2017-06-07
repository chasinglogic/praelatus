"""UI routes for tickets."""

from flask import request, session, redirect

from praelatus.app.ui.blueprint import ui
from praelatus.lib import connection
from praelatus.store import (ProjectStore, TicketStore, TicketTypeStore,
                             UserStore)
from praelatus.templates import render_template


@ui.route('/<string:project_key>/<string:ticket_key>')
def show_ticket(project_key, ticket_key):
    """Display a ticket's full detail."""
    with connection() as db:
        project = ProjectStore.get(db, actioning_user=session.get('user'),
                                   uid=project_key)
        ticket = TicketStore.get(db, actioning_user=session.get('user'),
                                 project=project, uid=ticket_key)
        return render_template('tickets/show.html', ticket=ticket)


@ui.route('/tickets/<project_key>/create', methods=('GET', 'POST'))
def create_ticket(project_key):
    """Create a ticket."""
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
        return render_template('tickets/create.html', project=project)
