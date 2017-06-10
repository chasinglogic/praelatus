from flask import session, request

from praelatus.lib import connection
from praelatus.store import ProjectStore
from praelatus.app.ui.forms import CreateProjectForm
from praelatus.app.ui.helpers import admin_required
from praelatus.app.ui.blueprint import ui
from praelatus.templates import render_template


@ui.route('/admin/system')
@admin_required
def system_info():
    return render_template('admin/sys_info.html')


@ui.route('/admin/projects')
# @admin_required
def project_sys_admin():
    with connection() as db:
        projects = ProjectStore.search(db, request.args.get('filter', '*'), actioning_user=session.get('user'))
        return render_template('admin/projects.html',
                               projects=projects)


@ui.route('/admin/projects/create')
# @admin_required
def project_create():
    with connection() as db:
        projects = ProjectStore.search(db, request.args.get('filter', '*'), actioning_user=session.get('user'))
        return render_template('admin/projects.html',
                               projects=projects)
