"""Execute hooks on a transition."""

import requests
import jinja2

from praelatus.tasks.app import app


@app.task
def fire_web_hooks(hooks, ticket):
    """Fire all hooks as web hooks for ticket.

    Hooks is an array of hook dict objects and ticket is a ticket dict
    object. Both as returned by jsonify()
    """
    results = []
    for h in hooks:
        b = jinja2.Template(h['body']).render(**ticket)
        r = requests.Request(h['method'], h['url'], data=b)
        with requests.Session() as s:
            res = s.send(r)
            results.append({
                'URL': h['url'],
                'Status': res.status_code,
                'Method': h['method'],
                'RequestBody': b,
                'ResponseBody': res.text
            })
    return results
