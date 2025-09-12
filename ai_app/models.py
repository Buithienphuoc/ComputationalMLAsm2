from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_data = models.JSONField()
    result = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} by {self.user.username}"

class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    team_avg_goals_per_match = models.FloatField(null=True, blank=True)
    team_avg_goals_conceded = models.FloatField(null=True, blank=True)
    team_clean_sheet_rate = models.FloatField(null=True, blank=True)
    matches_played = models.IntegerField(null=True, blank=True)
    goals_scored_total = models.IntegerField(null=True, blank=True)
    goals_conceded_total = models.IntegerField(null=True, blank=True)
    clean_sheets = models.IntegerField(null=True, blank=True)
    team_avg_shots = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    player_id = models.IntegerField(unique=True)  # from CSV
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    position_encoded = models.IntegerField(null=True, blank=True)

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players")

    minutes = models.FloatField(null=True, blank=True)
    appearances = models.FloatField(null=True, blank=True)
    goals = models.FloatField(null=True, blank=True)
    assists = models.FloatField(null=True, blank=True)
    shots_total = models.FloatField(null=True, blank=True)
    shots_on = models.FloatField(null=True, blank=True)
    passes_total = models.FloatField(null=True, blank=True)
    passes_key = models.FloatField(null=True, blank=True)

    avg_minutes_played = models.FloatField(null=True, blank=True)
    shots_per_game = models.FloatField(null=True, blank=True)
    conversion_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.team.name})"