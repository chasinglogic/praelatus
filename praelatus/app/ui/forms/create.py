from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms.validators import DataRequired

class CreateTicketForm(FlaskForm):
    """Used for validating the ticket form."""
    project_name = SelectField('Project Name', choices=[])
    summary = StringField('Summary', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
