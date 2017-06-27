# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-27 14:22
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0003_auto_20170627_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='watchers',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
