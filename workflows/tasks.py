import jinja2
import requests

from celery import shared_task
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@shared_task
def fire_hooks(transition, ticket):
    for h in transition.web_hooks:
        b = jinja2.Template(h.body).render(ticket)
        r = requests.Request(h.method, h.url, data=b)
        with requests.Connection() as s:
            res = s.send(r)
            log.info("%s: %s Status Code: %d Response: %s" %
                     (h.method, h.url, res.status_code, res.text))
