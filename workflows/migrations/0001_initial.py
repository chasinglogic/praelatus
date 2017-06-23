# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 20:21
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('state', models.CharField(choices=[('TODO', 'TODO'), ('IN_PROGRESS', 'IN_PROGRESS'), ('DONE', 'DONE')], default='TODO', max_length=11)),
                ('bg_color', models.CharField(max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Create', max_length=255)),
                ('from_status', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='workflows.Status')),
                ('to_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='workflows.Status')),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workflows.Status')),
            ],
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='workflows.Workflow'),
        ),
    ]
