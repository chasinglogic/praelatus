from celery import shared_task
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@shared_task
def fire_hooks(hooks, context):
    fire_web_hooks().delay(hooks, context)


@shared_task
def fire_web_hooks(web_hooks, context):
    for h in web_hooks:
        res = h.fire_hook(context)
        log.info("%s: %s Status Code: %d Response: %s" %
                 (h.method, h.url, res.status_code, res.text))
