from django.db import models
from datetime import time


class Team(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Stadium(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Event(models.Model):
    date = models.DateField(verbose_name='日付')
    home_team = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        null=True, 
        verbose_name='ホームチーム'  # verbose_name を追加
    )
    away_team = models.ForeignKey(
        Team, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='アウェイチーム',
        related_name='away_events'
    )
    stadium = models.ForeignKey(
        Stadium, 
        on_delete=models.CASCADE, 
        related_name='events', 
        null=True, 
        verbose_name='球場'  # verbose_name を追加
    )
    start_time = models.TimeField(verbose_name='試合開始時間', default=time(12, 0))
    score = models.CharField(max_length=100, blank=True, null=True)  
    comment = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"{self.date} - {self.home_team} vs {self.away_team} at {self.stadium}"


