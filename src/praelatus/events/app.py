"""The Celery app object."""

from celery import Celery

app = Celery('praelatus', backend='rpc://', broker='amqp://')
