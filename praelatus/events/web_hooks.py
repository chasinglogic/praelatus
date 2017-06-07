"""Execute hooks on a transition."""

import jinja2
import requests

from celery.utils.log import get_task_logger
from praelatus.events.app import app

logger = get_task_logger(__name__)


@app.task
def send_web_hooks(hooks, ticket):
    """Fire all hooks as web hooks for ticket.

    Hooks is an array of hook dict objects and ticket is a ticket dict
    object. Both as returned by jsonify()
    """
    for h in hooks:
        b = jinja2.Template(h['body']).render(**ticket)
        r = requests.Request(h['method'], h['url'], data=b)
        with requests.Connection() as s:
            res = s.send(r)
            logger.info("%s: %s StatusCode: %d Response: %s" %
                        (h['method'], h['url'], res.status_code, res.text))
