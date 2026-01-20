"""
URL configuration for RAG chatbot
"""

from django.urls import path
from . import views

urlpatterns = [
    path('api/chat/', views.chat_api, name='rag_chat_api'),
    path('api/health/', views.health_check, name='rag_health_check'),
]

