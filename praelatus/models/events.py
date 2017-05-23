"""Define the event class and related models."""

import enum


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
