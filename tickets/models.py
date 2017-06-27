from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template.loader import get_template
from notifications.models import Notification

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

    key = models.CharField(max_length=255, unique=True)
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

    fields = GenericRelation(FieldValue, related_query_name='ticket')
    labels = models.ManyToManyField(Label)
    watchers = models.ManyToManyField(User)

    def watching(self, filter_out=None):
        """Return all users who should be notified of actions on this ticket."""
        recipients = [self.assignee, self.reporter]
        if len(self.watchers.all()) > 0:
            recipients = recipients + self.watchers.all()
        if filter_out:
            recipients = [r for r in recipients if r not in filter_out]
        return recipients

    @property
    def transitions(self):
        """Get available transitions for a ticket."""
        return Transition.objects.\
            filter(
                Q(workflow=self.workflow,
                  from_status=self.status) |
                (Q(workflow=self.workflow, from_status=None) &
                 ~Q(to_status=self.status))
            ).\
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


class Upvote(models.Model):
    """An upvote on a ticket"""

    voter = models.ForeignKey(User)
    ticket = models.ForeignKey(Ticket, related_name='upvotes')
    created_at = models.DateTimeField(auto_now_add=True)


class FieldScheme(models.Model):
    """Determine what fields a project wants for a ticket type."""
    name = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(Project, related_name='field_schemes')
    ticket_type = models.ForeignKey(TicketType, related_name='field_schemes',
                                    blank=True, null=True)

    @classmethod
    def get_for_project(cls, project=None, **kwargs):
        schemes = cls.objects.filter(project=project, **kwargs)

        if len(schemes) == 0:
            schemes = cls.objects.filter(project=project, ticket_type=None)

        if len(schemes) > 0:
            return schemes[0]
        return None

    class Meta:
        unique_together = ('project', 'ticket_type',)

    def __str__(self):
        """Return the scheme's name."""
        return '%s for %s' % (self.name, self.project.name)


class FieldSchemeField(models.Model):
    """A field on a FieldScheme"""
    required = models.BooleanField(default=False)
    scheme = models.ForeignKey(FieldScheme, related_name='fields')
    field = models.ForeignKey(Field)

    class Meta:
        unique_together = ('scheme', 'field',)

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
    name = models.CharField(max_length=255, unique=True)
    project = models.ForeignKey(Project, related_name='workflow_schemes')
    workflow = models.ForeignKey(Workflow, related_name='schemes')
    ticket_type = models.ForeignKey(TicketType, related_name='workflow_schemes',
                                    null=True, blank=True)

    @classmethod
    def get_for_project(cls, project=None, **kwargs):
        schemes = cls.objects.filter(project=project, **kwargs)

        if len(schemes) == 0:
            schemes = cls.objects.filter(project=project, ticket_type=None)

        if len(schemes) > 0:
            return schemes[0]
        return None

    def __str__(self):
        """Return the scheme's name."""
        return '%s for %s' % (self.name, self.project.name)

    class Meta:
        unique_together = ('project', 'ticket_type', 'workflow',)


class Attachment(models.Model):
    """An attachment on a ticket."""
    ticket = models.ForeignKey(Ticket, related_name='attachments')
    uploader = models.ForeignKey(User, related_name='attachments')
    # Optional display name.
    name = models.CharField(max_length=255, null=True, blank=True)
    attachment = models.FileField(upload_to='tickets/attachments/')


class TicketLink(models.Model):
    """A link to an issue, docs, another ticket."""
    display = models.CharField(max_length=140)
    href = models.URLField()
    ticket = models.ForeignKey(Ticket, related_name='links')


@receiver(pre_save, sender=Notification)
def email_watchers(sender, instance=None, **kwargs):
    c = {
        'ticket': instance.action_object,
        'actor': instance.actor,
        'verb': instance.verb
    }

    if hasattr(instance, 'description') and instance.description != '':
        c['comment'] = instance.description
        html_content = get_template('email/html/comment.html').render(c)
        text_content = ''
    else:
        html_content = get_template('email/html/transition.html').render(c)
        text_content = get_template('email/text/transition.txt').render(c)

    msg = EmailMultiAlternatives(
        'Ticket Tracking System: ' + instance.action_object.key,
        text_content,
        settings.EMAIL_ADDRESS,
        [u.email for u in instance.action_object.watching()]
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
