from django.db import models


class Label(models.Model):
    """A generic label that mimics github labels to some degree."""
    name = models.CharField(max_length=100)
    bg_color = models.CharField(max_length=7)
