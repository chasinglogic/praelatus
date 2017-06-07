"""UI routes for projects."""

from flask import request, session

from praelatus.templates import render_template
from praelatus.store import ProjectStore
from praelatus.lib import connection
from praelatus.app.ui.blueprint import ui


@ui.route('/projects/search')
def search_projects():
    """Search projects."""
    with connection() as db:
        search = request.args.get('filter')
        if search == '' or search is None:
            search = '*'
        projects = ProjectStore.search(db, search=search,
                                       actioning_user=session.get('user'))
        return render_template('projects/search.html', projects=projects)


@ui.route('/<key>')
def show_project(key):
    """Show a single projects page."""
    with connection() as db:
        project = ProjectStore.get(db, uid=key,
                                   actioning_user=session.get('user'))
        if project:
            return render_template('web/projects/show.html', project=project)

        return render_template('404.html',
                               message='No project with that key was found.')
