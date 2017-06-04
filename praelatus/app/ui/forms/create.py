from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import TextAreaField
from wtforms import SelectField
from wtforms.validators import DataRequired

class CreateTicketForm(FlaskForm):
    """Used for validating the ticket form."""
    summary = StringField('Summary', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    # Change to a function that will pull a list of all available assignees
    # assignee = SelectField('Assignee', choices=[
    #     (None, 'None'),
    #     ('testuser', 'Moe'),
    #     ('curly', 'Curly'),
    #     ('larry', 'Larry')
    # ], validators=[DataRequired()])
    assignee = None
    # Change to a function that will pull a list of all available projects
    project_name = SelectField('Project Name', choices=[
        ('TEST', 'Ticket Type 1'),
        ('tt2', 'Ticket Type 2'),
        ('tt3', 'Ticket Type 3')
    ], validators=[DataRequired()])
    # Change to a function that will pull a list of all available ticket types
    ticket_type = SelectField('Ticket Type', choices=[
        ('Bug', 'Ticket Type 1'),
        ('tt2', 'Ticket Type 2'),
        ('tt3', 'Ticket Type 3')
    ], validators=[DataRequired()])
