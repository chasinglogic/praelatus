from django.db import models


class Workflow(models.Model):
    """A workflow is a set of statuses and transitions."""

    name = models.CharField(max_length=255)
    description = models.TextField()


class Status(models.Model):
    """A state in the process of a workflow."""

    name = models.CharField(max_length=255)
    # Hex color for the background of the Status Pill
    color = models.CharField(max_length=7)


class Transition(models.Model):
    """A transition from one status to another."""

    name = models.CharField(max_length=255, default='Create')
    workflow = models.ForeignKey(Workflow)
    to_status = models.ForeignKey(Status, related_name='+')
    from_status = models.ForeignKey(Status, related_name='+', null=True)
