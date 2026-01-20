from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import CustomLoginView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
