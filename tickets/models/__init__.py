"""The Ticket class and related models"""

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

from fields.models import FieldValue
from labels.models import Label
from projects.models import Project
from workflows.models import Status, Transition, Workflow

from .ticket_types import TicketType
from .links import Link
from .upvotes import Upvote


class Ticket(models.Model):
    """A unit of work."""

    key = models.CharField(max_length=255, unique=True)
    summary = models.CharField(max_length=140)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    project = models.ForeignKey(Project, related_name='content', on_delete=models.CASCADE)
    reporter = models.ForeignKey(User, related_name='reported', on_delete=models.PROTECT)
    assignee = models.ForeignKey(User, related_name='assigned', null=True,
                                 on_delete=models.SET_NULL)
    ticket_type = models.ForeignKey(TicketType, related_name='tickets',
                                    on_delete=models.PROTECT)
    status = models.ForeignKey(Status, default=1, related_name='tickets',
                               on_delete=models.PROTECT)
    workflow = models.ForeignKey(Workflow, default=1, related_name='tickets',
                                 on_delete=models.PROTECT)

    links = GenericRelation(Link, related_query_name='ticket')
    upvotes = GenericRelation(Upvote, related_query_name='ticket')
    fields = GenericRelation(FieldValue, related_query_name='ticket')
    labels = models.ManyToManyField(Label)
    watchers = models.ManyToManyField(User)

    parent = models.ForeignKey('self', null=True, related_name='tasks', on_delete=models.CASCADE)

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

    def ordered_parents(self):
        p = [x for x in self.parents()]
        return reversed(p)

    def parents(self):
        parent = self.parent
        while parent is not None:
            yield parent
            parent = parent.parent


class Comment(models.Model):
    """A comment on a ticket."""

    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


class Attachment(models.Model):
    """An attachment on a ticket."""
    ticket = models.ForeignKey(Ticket, related_name='attachments', on_delete=models.CASCADE)
    uploader = models.ForeignKey(User, related_name='attachments', on_delete=models.CASCADE)
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
