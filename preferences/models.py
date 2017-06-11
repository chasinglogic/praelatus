import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Preferences(models.Model):
    """A users preferences."""

    user = models.OneToOneField(User, related_name='preferences')
    avatar = models.CharField(max_length=255)
    gravatar = models.CharField(max_length=255)

    @property
    def profile_pic(self):
        if self.avatar and self.avatar != '':
            return self.avatar
        return self.gravatar


@receiver(post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    if created:
        preferences = Preferences.objects.create(user=instance)
        md5 = hashlib.md5()
        md5.update(instance.email.encode('utf-8'))
        preferences.gravatar = 'https://gravatar.com/avatar/' + md5.hexdigest()
        preferences.save()


@receiver(post_save, sender=User)
def save_user_preferences(sender, instance, **kwargs):
    instance.preferences.save()
