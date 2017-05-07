"""Fire hooks for a transition."""

import requests
import jinja2

from praelatus.tasks.app import app


@app.task
def fire_web_hooks(hooks, ticket):
    """Fire all hooks as web hooks for ticket.

    Hooks is an array of hook dict objects and ticket is a ticket dict
    object.  both as returned by clean_dict()
    """
    for h in hooks:
        b = jinja2.Template(h['body']).render(**ticket)
        r = requests.Request(h['method'], h['url'], data=b)
        with requests.Session() as s:
            s.send(r)
