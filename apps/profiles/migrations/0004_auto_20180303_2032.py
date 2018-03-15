# Generated by Django 2.0.1 on 2018-03-03 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_notification_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='notification_preference',
            field=models.CharField(choices=[('none', 'None'), ('email', 'Email')], default='email', max_length=140),
        ),
    ]