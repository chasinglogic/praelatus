import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """A users profile."""

    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255)
    gravatar = models.CharField(max_length=255)
    active = models.BooleanField(default=True)

    @property
    def profile_pic(self):
        if self.avatar and self.avatar != '':
            return self.avatar
        return self.gravatar


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        md5 = hashlib.md5()
        md5.update(instance.email.encode('utf-8'))
        profile.gravatar = 'https://gravatar.com/avatar/' + md5.hexdigest()
        profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    md5 = hashlib.md5()
    md5.update(instance.email.encode('utf-8'))
    instance.profile.gravatar = 'https://gravatar.com/avatar/' + md5.hexdigest(
    )
    instance.profile.save()
