"""Define the event class and related models."""

import enum

from praelatus.events.web_hooks import send_web_hooks
from praelatus.events.notications import send_email


class EventType(enum.Enum):
    """Available event types in Praelatus."""
    COMMENT_ADDED = 'COMMENT_ADDED'
    TRANSITION = 'TRANSITION'


class Event:
    """Represents and instance of an event."""

    def __init__(self, user, ticket, transition=None, comment=None):
        """Create an event caused by user for ticket.

        Either transition or commment must be passed as appropriate, otherwise
        a TypeError is raised.
        """
        if comment is not None:
            self.event_type = EventType.COMMENT_ADDED
            self.comment = comment
        elif transition is not None:
            self.event_type = EventType.TRANSITION
            self.transition = transition
        else:
            raise TypeError('No valid data passed')

        self.user = user
        self.ticket = ticket


# TODO send to websocket listeners
# TODO pull recipients from the database
def send_event(event):
    """Send event to all appropriate listeners.

    event should be an instance of the Event class.
    """
    if event.event_type == EventType.TRANSITION:
        web_hooks = filter(lambda x: x, event.transition.hooks)
        send_web_hooks.delay(web_hooks, event.ticket)
    send_email([], event)
