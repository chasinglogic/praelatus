"""Hooks that get fired on Workflow transitions."""

from urllib.request import getproxies

import jinja2
import requests
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Hook(models.Model):
    """The base hook class, use WebHook or ScriptHook instead."""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class WebHook(Hook):
    """WebHooks are fired at endpoints with an optional context.

    The URL and body are jinja2 templates.
    """
    name = models.CharField(max_length=255)
    url = models.TextField()
    body = models.TextField(null=True, blank=True)
    method = models.CharField(max_length=10, default='POST')

    def fire_hook(self, context=None, verify=True, timeout=5):
        """Render the url and body then send the request, returns the response."""
        rendered_body = jinja2.Template(self.body).render(context)
        rendered_url = jinja2.Template(self.url).render(context)
        req = requests.Request(self.method, rendered_url, data=rendered_body)
        with requests.Session() as sess:
            res = sess.send(req.prepare(),
                            timeout=timeout,
                            verify=verify,
                            proxies=getproxies())
            return res

    def __str__(self):
        """Return name."""
        return self.name
