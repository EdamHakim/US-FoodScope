from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_env_view, name='food_env'),
    path('predict/', views.food_env_predict, name='food_env_predict'),
    path('clustering/', views.food_env_clustering, name='food_env_clustering')

]