
# Create your models here.
"""
Finance Prediction Models
Stores prediction history for tax rate and clustering predictions
"""
from django.db import models
from django.conf import settings

class PredictionHistory(models.Model):
    """Store finance prediction history"""
    MODEL_CHOICES = [
        ('tax_rate', 'Tax Rate'),
        ('clustering', 'State Clustering'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='finance_predictions'
    )
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    prediction_value = models.FloatField(help_text="Predicted tax rate or cluster number")
    input_data = models.JSONField(default=dict, blank=True, help_text="Full form input data")
    confidence_interval = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Confidence or risk level"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.model_type} - {self.created_at.strftime('%Y-%m-%d')}"