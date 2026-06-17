from django.db import models
from django.contrib.auth.models import User
from users.models import Game

class Review(models.Model):
    # Store game reviews with star ratings (1-5)
    RATING_CHOICES = [
        (1, '★☆☆☆☆'),
        (2, '★★☆☆☆'),
        (3, '★★★☆☆'),
        (4, '★★★★☆'),
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
        # Display the review as "username's review of gamename" for easy identification
        return f"{self.user.username}'s review of {self.game.title}"


