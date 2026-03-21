from django.urls import path
from . import views

app_name = 'ai_assistant'

urlpatterns = [
    path('', views.AIAssistantIndexView.as_view(), name='index'),
    path('dashboard/', views.AIAssistantDashboardView.as_view(), name='dashboard'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('api/config/', views.config_api, name='config_api'),
    path('api/clear-history/', views.clear_history, name='clear_history'),
    path('api/feedback/', views.feedback_api, name='feedback_api'),
]
