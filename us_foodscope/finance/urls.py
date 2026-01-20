"""
Finance URL Configuration
"""
from django.urls import path
from . import views

urlpatterns = [
    # Main prediction page
    path('', views.finance_view, name='finance'),

    # Clustering visualization
    path('clustering/', views.clustering_view, name='finance_clustering'),
    
    # API endpoint for clustering data
    path('api/clustering-data/', views.clustering_data_api, name='clustering_data'),
]