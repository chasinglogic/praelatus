"""Models for the Workflows App"""

import enum

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from .hooks import WebHook


class State(enum.Enum):
    """Indicates whether a Status is ToDo, In Progress, or Done."""
    TODO = 'TODO'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'


class Status(models.Model):
    """A state in the process of a workflow."""
    name = models.CharField(max_length=255, unique=True)
    state = models.CharField(max_length=11, default=State.TODO.value,
                             choices=[(x.value, x.value) for x in State])

    @property
    def is_todo(self):
        """Indicate if this is a waiting to be worked status."""
        return self.state == State.TODO.value

    @property
    def is_in_progress(self):
        """Indicate if this is a being worked status."""
        return self.state == State.IN_PROGRESS.value

    @property
    def is_done(self):
        """Indicate if this is a completed status."""
        return self.state == State.DONE.value

    def __str__(self):
        """Return name."""
        return self.name


class Workflow(models.Model):
    """A workflow is a set of statuses and transitions."""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    create_status = models.ForeignKey(Status, on_delete=models.PROTECT)
    web_hooks = GenericRelation(WebHook)

    def __str__(self):
        """Return name."""
        return self.name


class Transition(models.Model):
    """A transition from one status to another."""
    name = models.CharField(max_length=255)
    workflow = models.ForeignKey(Workflow, related_name='transitions', on_delete=models.CASCADE)
    to_status = models.ForeignKey(Status, related_name='+', on_delete=models.PROTECT)
    from_status = models.ForeignKey(Status, related_name='+', null=True, blank=True, on_delete=models.PROTECT)
    web_hooks = GenericRelation(WebHook)

    def __str__(self):
        """Return name."""
        return self.name
