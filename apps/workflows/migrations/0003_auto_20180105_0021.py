# Generated by Django 2.0.1 on 2018-01-05 00:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('workflows', '0002_auto_20180104_1955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='WebHook',
            fields=[
                ('hook_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='workflows.Hook')),
                ('name', models.CharField(max_length=255)),
                ('url', models.TextField()),
                ('body', models.TextField(blank=True, null=True)),
                ('method', models.CharField(default='POST', max_length=10)),
            ],
            bases=('workflows.hook',),
        ),
        migrations.AddField(
            model_name='hook',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]
