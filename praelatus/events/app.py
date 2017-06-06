"""The Celery app object."""

from celery import Celery
from praelatus.config import config

app = Celery('praelatus', broker=config.mq_server)
