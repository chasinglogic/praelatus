# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-14 16:24
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('queries', '0002_auto_20170713_1816'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueryUse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_used', models.DateTimeField(auto_now_add=True)),
                ('query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='queries.Query')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='queryuse',
            unique_together=set([('user', 'query')]),
        ),
    ]
