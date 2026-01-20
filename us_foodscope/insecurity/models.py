from django.db import models
from django.conf import settings

class FoodInsecurityPredictionHistory(models.Model):
    """
    Track food insecurity predictions for users.
    Stores input features and prediction results.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insecurity_predictions')
    
    # Prediction result
    prediction_value = models.FloatField(help_text="Predicted food insecurity risk score (0-1)")
    risk_level = models.CharField(max_length=20, choices=[
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
    ])
    
    # Input data (full feature set)
    input_data = models.JSONField(default=dict, blank=True, help_text="Full form input data")
    
    # Metadata
    confidence = models.FloatField(default=0.0, help_text="Model confidence score")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Food Insecurity Prediction'
        verbose_name_plural = 'Food Insecurity Predictions'
    
    def __str__(self):
        return f"{self.user.username} - {self.risk_level} - {self.created_at.strftime('%Y-%m-%d')}"
