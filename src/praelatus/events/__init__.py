"""Holds the Celery app object and tasks for Praelatus."""
# flake8: noqa
from praelatus.events.event import Event
from praelatus.events.event import EventType
from praelatus.events.event import EventManager
from praelatus.events.notifications import send_email
from praelatus.events.web_hooks import send_web_hooks


mgr = EventManager
mgr.register_listener(lambda _: True, send_email)
mgr.register_listener(lambda x: x.event_type == EventType.TRANSITION,
                      send_web_hooks)


def send_event(event):
    """Alias for the module EventManager instance."""
    mgr.send_event(event)
