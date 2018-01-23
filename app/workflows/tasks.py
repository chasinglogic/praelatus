"""Celery tasks for firing Workflow hooks"""

from celery import shared_task
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


@shared_task
def fire_hooks(hooks, context):
    """Given an array of hooks will fire the appropriate celery task for all of
    them.
    """
    fire_web_hooks.delay(hooks, context)


@shared_task
def fire_web_hooks(web_hooks, context):
    """Given an array of web_hooks will send the requests in order rendering
    the context.
    """
    for hook in web_hooks:
        res = hook.fire_hook(context)
        logger.info("%s: %s Status Code: %d Response: %s",
                    hook.method, hook.url, res.status_code, res.text)
