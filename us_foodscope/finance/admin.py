
# Register your models here.
"""
Finance Admin Configuration
"""
from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'model_type', 'prediction_value', 'created_at']
    list_filter = ['model_type', 'created_at']
    search_fields = ['user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    def has_add_permission(self, request):
        # History is created automatically, not manually
        return False