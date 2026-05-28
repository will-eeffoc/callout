from django.db import models
from django.contrib.auth.models import User
from users.models import Game

class Review(models.Model):
    RATING_CHOICES = [
        (0.5, '★☆☆☆☆'),
        (1, '★☆☆☆☆'),
        (1.5, '★★☆☆☆'),
        (2, '★★☆☆☆'),
        (2.5, '★★★☆☆'),
        (3, '★★★☆☆'),
        (3.5, '★★★★☆'),
        (4, '★★★★☆'),
        (4.5, '★★★★★'),
        (5, '★★★★★'),
    ]
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_reviews')
    rating = models.DecimalField(max_digits=2, decimal_places=1, choices=RATING_CHOICES)
    text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('game', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.game.title}"


