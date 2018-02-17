from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template

from celery import shared_task
from celery.utils.log import get_task_logger
from profiles.serializers import UserSerializer

from .models import Activity, Notification
from .serializers import ActivitySerializer

logger = get_task_logger(__name__)


def format_template_string(activity):
    tmpl = ''
    if activity.type == Activity.Transition:
        tmpl = '{user} transitioned {ticket} to {status}'
    elif activity.type == Activity.Comment:
        tmpl = '{user} commented on {ticket}'

    return tmpl.format(user=activity.actioning_user.username,
                       ticket=activity.ticket.key,
                       status=activity.ticket.status.name)


@receiver(post_save, sender=Activity)
def notify_watchers(sender, instance=Activity(), **kwargs):
    watchers = list(instance.ticket.watchers.all()) + \
        list(instance.project.watchers.all())
    watchers.append(instance.ticket.reporter)
    if instance.ticket.assignee is not None:
        watchers.append(instance.ticket.assignee)

    for watcher in watchers:
        send_notification.delay(UserSerializer(watcher).data,
                                ActivitySerializer(instance).data)


@shared_task
def send_notification(user, activity):
    user = User.objects.filter(id=user['id']).first()
    activity = Activity.objects.filter(id=activity['id']).first()

    if user.id == activity.actioning_user.id:
        return

    notification = Notification(
        user=user,
        activity=activity,
        body=format_template_string(activity)
    )

    notification.save()

    if user.profile.notification_preference == 'email':
        email_notification(user, notification)


def email_notification(user, notification):
    ctx = {
        'ticket': notification.activity.ticket,
        'actor': notification.activity.actioning_user,
        'watcher': user,
        'action_object': notification.activity.content_object
    }

    html_content = ''
    text_content = ''

    if notification.activity.type == Activity.Comment:
        html_content = get_template('email/html/comment.html').render(ctx)
        text_content = get_template('email/text/comment.txt').render(ctx)
    elif notification.activity.type == Activity.Transition:
        html_content = get_template('email/html/transition.html').render(ctx)
        text_content = get_template('email/text/transition.txt').render(ctx)
    else:
        # Unknown activity type no email required.
        return

    msg = EmailMultiAlternatives(
        'Ticket Tracking System: ' +
        ctx['ticket'].key + ' ' +
        format_template_string(notification.activity),
        text_content,
        settings.EMAIL_ADDRESS,
        user.email)

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
