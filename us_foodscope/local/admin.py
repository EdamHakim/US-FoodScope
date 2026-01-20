from django.contrib import admin
from .models import RegressionPredictionHistory


@admin.register(RegressionPredictionHistory)
class RegressionPredictionHistoryAdmin(admin.ModelAdmin):
    """Admin interface for regression prediction history."""
    
    list_display = (
        'user',
        'prediction_value',
        'cluster_assigned',
        'cluster_probability',
        'created_at'
    )
    
    list_filter = (
        'created_at',
        'cluster_assigned',
        'user'
    )
    
    search_fields = (
        'user__username',
        'user__email'
    )
    
    readonly_fields = (
        'user',
        'input_data',
        'prediction_value',
        'confidence_score',
        'cluster_assigned',
        'cluster_probability',
        'created_at',
        'updated_at'
    )
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'created_at', 'updated_at')
        }),
        ('Input Data', {
            'fields': ('input_data',),
            'classes': ('collapse',)
        }),
        ('Regression Results', {
            'fields': ('prediction_value', 'confidence_score')
        }),
        ('Clustering Results', {
            'fields': ('cluster_assigned', 'cluster_probability')
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition - only created via predictions."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deletion only for superusers."""
        return request.user.is_superuser
