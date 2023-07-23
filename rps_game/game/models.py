from django.db import models
from django.contrib.auth.models import User

#Score model to save scores and highscores to the database
class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    highest_streak = models.PositiveIntegerField(default=0)

    # For displaying in the webpage
    def __str__(self):
            return f"{self.user.username}'s Score: {self.score}"