"""Blueprint for the user facing half of Praelatus."""

from flask import session, redirect, Blueprint

from praelatus.app.ui.forms import RegisterForm
from praelatus.templates import render_template

ui = Blueprint('ui', __name__)


@ui.route('/')
def index():
    """Show either the welcome screen or dashboard."""
    if session.get('user'):
        return redirect('/dashboard')
    return render_template('index.html', form=RegisterForm(),
                           action='/register', submit_value='Sign Up')
