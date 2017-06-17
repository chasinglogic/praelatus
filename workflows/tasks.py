from celery import shared_task
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@shared_task
def fire_hooks(transition, ticket):
    fire_web_hooks(transition, ticket).delay()


@shared_task
def fire_web_hooks(transition, ticket):
    for h in transition.web_hooks.all():
        res = h.fire_hook(ticket)
        log.info("%s: %s Status Code: %d Response: %s" %
                 (h.method, h.url, res.status_code, res.text))
