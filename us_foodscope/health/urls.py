from django.urls import path
from . import views

urlpatterns = [
    path('', views.health_view, name='health'),
    path('clustering/', views.clustering_view, name='health_clustering'),
    path('clustering/api/', views.clustering_data_api, name='health_clustering_api'),
]

