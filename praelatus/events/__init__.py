"""Holds the Celery app object and tasks for Praelatus."""
# flake8: noqa
from praelatus.events.app import app
from praelatus.events.web_hooks import fire_web_hooks
