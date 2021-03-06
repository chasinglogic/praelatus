# Generated by Django 2.0.1 on 2018-03-03 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='type_of_activity',
            new_name='type',
        ),
        migrations.AddField(
            model_name='activity',
            name='content_type',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='body',
            field=models.CharField(default='', max_length=140),
            preserve_default=False,
        ),
    ]
