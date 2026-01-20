from django.db import models
from django.conf import settings

class AccessPredictionHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    input_data = models.JSONField()
    prediction_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Access Prediction ({self.user}) - {self.created_at:%Y-%m-%d %H:%M}"
