import jinja2
import requests

from urllib.request import getproxies
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


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

    def fire_hook(self, context={}, verify=True, timeout=5):
        """Render the url and body then send the request, returns the response."""
        b = jinja2.Template(self.body).render(context)
        u = jinja2.Template(self.url).render(context)
        r = requests.Request(self.method, u, data=b)
        with requests.Session() as s:
            res = s.send(r.prepare(),
                         timeout=timeout,
                         verify=verify,
                         proxies=getproxies())
            return res

    def __str__(self):
        """Return name."""
        return self.name
