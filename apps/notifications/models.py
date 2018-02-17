from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project
from tickets.models import Comment, Ticket


class Activity(models.Model):
    """Any activity that happens on a ticket or project."""
    project = models.ForeignKey(
        Project, related_name='activity', on_delete=models.CASCADE)
    ticket = models.ForeignKey(
        Ticket, related_name='history', on_delete=models.CASCADE)
    actioning_user = models.ForeignKey(
        User, related_name='activity', on_delete=models.CASCADE)
    type = models.CharField(max_length=140)

    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    Transition = 'TRANSITION'
    Comment = 'COMMENT'
    Create = 'CREATE'


class Notification(models.Model):
    """A notification for a user that needs to be acknowledged or mailed out."""
    user = models.ForeignKey(
        User, related_name='notifications', on_delete=models.CASCADE)
    activity = models.ForeignKey(
        Activity, related_name='notifications', on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    acknowledged = models.BooleanField(default=False)
    sent = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Comment)
def log_comment_activity(sender, instance=Comment(), **kwargs):
    if kwargs['created']:
        Activity(
            project=instance.ticket.project,
            ticket=instance.ticket,
            actioning_user=instance.author,
            type=Activity.Comment
        ).save()



@receiver(post_save, sender=Ticket)
def log_create_activity(sender, instance=Ticket(), **kwargs):
    if kwargs['created']:
        Activity(
            project=instance.project,
            ticket=instance,
            actioning_user=instance.reporter,
            type=Activity.Create
        ).save()
