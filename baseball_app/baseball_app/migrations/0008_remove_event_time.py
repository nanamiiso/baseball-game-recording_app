# Generated by Django 5.0.1 on 2024-02-23 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0007_remove_event_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
    ]