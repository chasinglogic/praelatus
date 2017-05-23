"""Holds the Celery app object and tasks for Praelatus."""
# flake8: noqa
from praelatus.tasks.app import app
from praelatus.tasks.web_hooks import fire_web_hooks
