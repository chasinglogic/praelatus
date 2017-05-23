import smtplib
from email.mime.text import MIMEText
import jinja2
from praelatus.models.events import EventType
from praelatus.models.events import Event
from praelatus.models import *

comment_template = jinja2.Template("""
Your home slice {{ user.full_name }} commented on {{ ticket.key }}:

{{ comment.body }}
""")

transition_template = jinja2.Template("""
{{ ticket.key }} has moved from {{ transition.from_status.name }} to
{{ transition.to_status.name }}
""")

def send_email(recipients, event):
    """Sends an email using the desired template"""
    subject = 'default'
    body = 'default'

    if event.event_type == EventType.COMMENT_ADDED:
        subject = '%s comment added' % (event.ticket.key)
        body = comment_template.\
            render(ticket=event.ticket,
                   user=event.user,
                   comment=event.comment)
    elif event.event_type == EventType.COMMENT_ADDED:
        subject = event.ticket

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = recipients
    msg['From'] = 'Mat'

    print(msg)

if __name__ == '__main__':
    u = User(**{
            'username': 'testadmin',
            'password': 'test',
            'email': 'test@example.com',
            'full_name': 'Test Testerson',
            'is_admin': True,
        })
    e = Event(
        u,
        Ticket(**{
            'key': 'TEST-1',
            'summary': 'This is a ticket',
            'description': 'This is a test',
            'workflow_id': 1,
            'reporter': u,
            'assignee': u,
            'status': Status(name='Backlog'),
            'project': Project(key='TEST',
                               name='TEST PROJ'),
        }),
        comment=Comment(
            author=u,
            body='This is a test comment.'
        )
    )

    send_email('ryan.brzezinski867@gmail.com', e)
