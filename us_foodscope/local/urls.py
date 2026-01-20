from django.urls import path
from . import views

urlpatterns = [
    path('', views.local_view, name='local'),
    path('regression/', views.local_regression_view, name='local_regression'),
    path('clustering/', views.local_clustering_view, name='local_clustering'),
    path('api/clustering-map/', views.clustering_map_view, name='clustering_map'),
]
