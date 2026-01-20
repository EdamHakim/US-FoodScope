from django.db import models
from django.conf import settings

class PredictionHistory(models.Model):
    MODEL_CHOICES = [
        ('obesity', 'Obesity'),
        ('diabetes', 'Diabetes'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_predictions')
    model_type = models.CharField(max_length=20, choices=MODEL_CHOICES)
    prediction_value = models.FloatField(help_text="Predicted percentage")
    risk_level_input = models.CharField(max_length=50, help_text="Risk Level input used")
    input_data = models.JSONField(default=dict, blank=True, help_text="Full form input data")
    confidence_interval = models.CharField(max_length=100, blank=True, null=True, help_text="CONFIDENCE INTERVAL STRING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.model_type} - {self.created_at.strftime('%Y-%m-%d')}"
