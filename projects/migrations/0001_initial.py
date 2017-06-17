# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 18:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=140)),
                ('key', models.CharField(max_length=10)),
                ('description', models.TextField()),
                ('icon_url', models.CharField(max_length=255)),
                ('homepage', models.CharField(max_length=255)),
                ('repo', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('admin_project', 'Ability to admin the project.'), ('view_project', 'Ability to view the project.'), ('create_content', 'Ability to create content within the project.'), ('edit_content', 'Ability to edit content within the project.'), ('comment_content', 'Ability to comment on content within the project.')),
            },
        ),
    ]
