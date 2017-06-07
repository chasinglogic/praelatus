from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired


class CreateTicketForm(FlaskForm):
    """Used for validating the ticket form."""
    project_name = SelectField('Project Name', choices=[])
    summary = StringField('Summary', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])


class CreateProjectForm(FlaskForm):
    """Used for validating the create project form."""
    name = StringField('Name', validates=[DataRequired()])
    description = TextAreaField('Name', validates=[DataRequired()])
    description = TextAreaField('Name', validates=[DataRequired()])
