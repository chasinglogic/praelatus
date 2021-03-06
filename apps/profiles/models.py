# Copyright 2018 Mathew Robinson <chasinglogic@gmail.com>. All rights reserved.
# Use of this source code is governed by the AGPLv3 license that can be found in
# the LICENSE file.

import hashlib

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """A users profile."""

    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255)
    gravatar = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    notification_preference = models.CharField(
        default='email',
        max_length=140,
        choices=[
            ('none', 'None'),
            ('email', 'Email')
        ])

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
