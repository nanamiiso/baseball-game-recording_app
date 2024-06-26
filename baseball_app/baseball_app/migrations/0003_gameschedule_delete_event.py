# Generated by Django 5.0.1 on 2024-02-09 06:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseball_app', '0002_event_description_event_end_time_event_start_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_date', models.DateField()),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='baseball_app.team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='baseball_app.team')),
                ('stadium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='baseball_app.stadium')),
            ],
        ),
        migrations.DeleteModel(
            name='Event',
        ),
    ]
