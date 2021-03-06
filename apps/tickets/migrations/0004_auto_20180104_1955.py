# Generated by Django 2.0.1 on 2018-01-04 19:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_ticket_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='assignee',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='reporter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reported', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='workflows.Status'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='tickets.TicketType'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='workflow',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets', to='workflows.Workflow'),
        ),
    ]
