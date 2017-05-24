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


class EventManager():
    """Manages listeners for events.

    A listener is any function which takes a single argument event which is an
    instance of the Event class.
    """

    def register_listener(self, filter_, listener):
        """Register listener with event manager.

        When filter_ is true call listener. filter_ is often an anonymous
        function. For example:

        lambda x: x.event_type == EventType.COMMENT_ADDED

        When send_event is called the EventManager's internal list of listeners
        will be filtered for listeners whose filter_ is true and then execute
        those listeners.
        """
        self.listeners.append({
            'filter': filter_,
            'listener': listener
        })

    def send_event(self, event):
        """Send event to all appropriate listeners.

        event should be an instance of the Event class.
        """
        matched = filter(lambda x: x['filter'](event), self.listeners)
        for m in matched:
            m(event)
