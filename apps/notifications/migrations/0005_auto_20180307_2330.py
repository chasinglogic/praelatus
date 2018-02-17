# Generated by Django 2.0.1 on 2018-03-07 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_auto_20180307_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
        migrations.AlterField(
            model_name='activity',
            name='object_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
