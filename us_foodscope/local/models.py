from django.db import models
from django.conf import settings


class RegressionPredictionHistory(models.Model):
    """Model to store regression prediction history for local food analysis."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='local_regression_predictions'
    )
    
    # Input features stored as JSON
    input_data = models.JSONField(default=dict, blank=True, help_text="Full form input data")
    
    # Prediction results
    prediction_value = models.FloatField(help_text="Predicted value from regression model")
    confidence_score = models.FloatField(null=True, blank=True, help_text="Model confidence/R² score")
    
    # Clustering results
    cluster_assigned = models.IntegerField(null=True, blank=True, help_text="Cluster assignment")
    cluster_probability = models.FloatField(null=True, blank=True, help_text="Probability of cluster assignment")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Regression Prediction Histories"
    
    def __str__(self):
        return f"{self.user.username} - Regression - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
