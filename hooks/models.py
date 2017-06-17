import jinja2
import requests

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
    method = models.CharField(max_length=10, default='POST')
    body = models.TextField(null=True, blank=True)

    def fire_hook(self, context={}):
        """Render the url and body then send the request, returns the response."""
        b = jinja2.Template(self.body).render(context)
        u = jinja2.Template(self.url).render(context)
        r = requests.Request(self.method, u, data=b)
        with requests.Connection() as s:
            res = s.send(r)
            return res

    def __str__(self):
        """Return name."""
        return self.name
