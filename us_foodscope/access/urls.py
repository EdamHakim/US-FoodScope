from django.urls import path
from . import views

app_name = "access"

urlpatterns = [
    path("", views.access_home, name="home"),
    path("prediction/", views.access_prediction, name="prediction"),
    path("clustering/", views.access_clustering, name="clustering"),
    path("clustering/clear/", views.access_clustering_clear, name="clustering_clear"),
]
