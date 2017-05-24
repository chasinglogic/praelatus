import smtplib

from jinja2 import Template
from pkg_resources import resource_string
from pkg_resources import resource_exists
from email.mime.text import MIMEText
from praelatus.events.event import EventType
from praelatus.events.event import Event
from praelatus.models import *


print(resource_exists('praelatus', 'templates/email/html/comment.html'))
print(resource_string('praelatus', 'templates/email/html/comment.html'))

templates = {
    'html': {
        'comment': Template(resource_string('praelatus', 'templates/email/html/comment.html')),
        # 'transition': resource_string('praelatus', 'templates/email/html/transition.html')
    },
    'text': {}
}

mta = smtplib.SMTP('praelatus.io', 587)

transition_template = Template("""
{{ ticket.key }} has moved from {{ transition.from_status.name }} to
{{ transition.to_status.name }}
""")


def send_email(recipients, event):
    """Sends an email using the desired template"""
    subject = 'default'
    body = 'default'

    if event.event_type == EventType.COMMENT_ADDED:
        subject = '%s comment added' % (event.ticket.key)
        body = templates['html']['comment'].\
            render(ticket=event.ticket,
                   user=event.user,
                   comment=event.comment)
    elif event.event_type == EventType.COMMENT_ADDED:
        subject = event.ticket

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['To'] = recipients
    msg['From'] = 'mrobinson@praelatus.io'
    print(msg)
    mta.send_message(msg)


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

    send_email('ryan.brzezinski867@gmail.com;mrobinson@praelatus.io', e)
