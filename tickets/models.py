from django.contrib.auth.models import User
from projects.models import Project
from labels.models import Label
from workflows.models import Workflow, Status, Transition
from django.db import models


class TicketType(models.Model):
    """A classification of a ticket, i.e. Bug, Feature, Epic."""

    name = models.CharField(max_length=255)


class Ticket(models.Model):
    """A unit of work."""

    key = models.CharField(max_length=255)
    summary = models.CharField(max_length=140)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(Project, related_name='content')
    reporter = models.ForeignKey(User, related_name='reported')
    assignee = models.ForeignKey(User, related_name='assigned')
    ticket_type = models.ForeignKey(TicketType, related_name='tickets')
    status = models.ForeignKey(Status, default=1, related_name='tickets')
    workflow = models.ForeignKey(Workflow, default=1, related_name='tickets')

    labels = models.ManyToManyField(Label)

    @property
    def transitions(self):
        """Get available transitions for a ticket."""
        return Transition.objects.\
            filter(workflow=self.workflow,
                   from_status=self.status).\
            all()


class Comment(models.Model):
    """A comment on a ticket."""

    body = models.TextField()
    author = models.ForeignKey(User)
    ticket = models.ForeignKey(Ticket, related_name='comments')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
