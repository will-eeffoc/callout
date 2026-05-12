from django.db import models
from django.contrib.auth.models import User

# transaction model: logs all financial activity (top-ups and contributions)
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chipin_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # positive for income, negative for expenses
    description = models.CharField(max_length=255)  # what triggered this transaction
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.description} - ${self.amount} on {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"

