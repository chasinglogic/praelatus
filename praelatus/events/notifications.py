"""Send notifications across various formats."""

import smtplib

from email.mime.text import MIMEText
from praelatus.events.event import EventType
from praelatus.templates import load_template
from praelatus.config import config


templates = {
    'html': {
        'comment': load_template('email/html/comment.html'),
        # 'transition': resource_string('praelatus', 'templates/email/html/transition.html')
    },
    'text': {}
}

(host, port) = config.smtp_server.split(':')
mta = smtplib.SMTP(host, int(port))


def send_email(recipients, event):
    """Send an email using the appropriate template based on event."""
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
    msg['From'] = config.email_address
    print(msg)
