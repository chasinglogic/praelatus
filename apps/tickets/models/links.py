from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Link(models.Model):
    """A link to an issue, docs, another ticket."""
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    display = models.CharField(max_length=140)
    href = models.URLField()

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
