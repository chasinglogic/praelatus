"""Define the app instance."""

import celery
from praelatus.config import config

app = celery.Celery('prae_tasks', broker=config.mq_server)
