from praelatus.app.ui.helpers import admin_required
from praelatus.app.ui.blueprint import ui
from praelatus.templates import render_template


@ui.route('/admin/system')
@admin_required
def system_info():
    return render_template('admin/sys_info.html')
