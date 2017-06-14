from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from fields.models import Field, FieldValue
from labels.models import Label
from projects.models import Project
from workflows.models import Status, Transition, Workflow


class TicketType(models.Model):
    """A classification of a ticket, i.e. Bug, Feature, Epic."""

    name = models.CharField(max_length=255)

    def __str__(self):
        """Return the type's name."""
        return self.name


class Ticket(models.Model):
    """A unit of work."""

    key = models.CharField(max_length=255)
    summary = models.CharField(max_length=140)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(Project, related_name='content')
    reporter = models.ForeignKey(User, related_name='reported')
    assignee = models.ForeignKey(User, related_name='assigned', null=True)
    ticket_type = models.ForeignKey(TicketType, related_name='tickets')
    status = models.ForeignKey(Status, default=1, related_name='tickets')
    workflow = models.ForeignKey(Workflow, default=1, related_name='tickets')

    fields = GenericRelation(FieldValue)
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

    class Meta:
        ordering = ['created_at']


class FieldScheme(models.Model):
    """Determine what fields a project wants for a ticket type."""
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='field_schemes')
    ticket_type = models.ForeignKey(TicketType, related_name='field_schemes',
                                    blank=True, null=True)

    def __str__(self):
        """Return the scheme's name."""
        return '%s for %s' % (self.name, self.project.name)


class FieldSchemeField(models.Model):
    """A field on a FieldScheme"""
    required = models.BooleanField(default=False)
    scheme = models.ForeignKey(FieldScheme, related_name='fields')
    field = models.ForeignKey(Field)

    @property
    def name(self):
        return self.field.name

    @property
    def options(self):
        return self.field.options

    @property
    def data_type(self):
        return self.field.data_type


class WorkflowScheme(models.Model):
    """Tie a workflow to a project for a TicketType."""
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, related_name='workflow_schemes')
    ticket_type = models.ForeignKey(TicketType, related_name='workflow_schemes',
                                    null=True, blank=True)
    workflow = models.ForeignKey(Workflow, related_name='schemes')

    def __str__(self):
        """Return the scheme's name."""
        return '%s for %s' % (self.name, self.project.name)
