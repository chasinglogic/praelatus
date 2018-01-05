from django.db import models
from projects.models import Project

class TicketType(models.Model):
    """A classification of a ticket, i.e. Bug, Feature, Epic."""

    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, related_name='ticket_types')

    def __str__(self):
        """Return the type's name."""
        return self.name

