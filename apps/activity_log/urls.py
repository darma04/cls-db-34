from django.urls import path
from . import views

app_name = 'activity_log'

urlpatterns = [
    path('', views.ActivityLogIndexView.as_view(), name='index'),
]
