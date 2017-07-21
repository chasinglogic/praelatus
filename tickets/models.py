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

from links.models import Link
from upvotes.models import Upvote
from fields.models import FieldValue
from labels.models import Label
from projects.models import Project
from workflows.models import Status, Transition, Workflow


class TicketType(models.Model):
    """A classification of a ticket, i.e. Bug, Feature, Epic."""

    name = models.CharField(max_length=255)
    projects = models.ManyToManyField(Project, related_name='ticket_types')

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

    links = GenericRelation(Link, related_query_name='ticket')
    upvotes = GenericRelation(Upvote, related_query_name='ticket')
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


class Attachment(models.Model):
    """An attachment on a ticket."""
    ticket = models.ForeignKey(Ticket, related_name='attachments')
    uploader = models.ForeignKey(User, related_name='attachments')
    # Optional display name.
    name = models.CharField(max_length=255, null=True, blank=True)
    attachment = models.FileField(upload_to='tickets/attachments/')


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
        'Ticket Tracking System: ' + instance.action_object.key, text_content,
        settings.EMAIL_ADDRESS,
        [u.email for u in instance.action_object.watching()])

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
