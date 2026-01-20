from django.urls import path
from . import views

urlpatterns = [
    path('', views.insecurity_view, name='insecurity'),
    path("clustering/", views.food_clustering_view, name="food_clustering"),
    path("clustering/api/", views.clustering_data_api, name="food_clustering_api"),
]

