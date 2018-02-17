from django.db import models


class Label(models.Model):
    """A generic label that mimics github labels to some degree."""
    name = models.CharField(max_length=100, unique=True)
    bg_color = models.CharField(max_length=7, default='#703D6F')
