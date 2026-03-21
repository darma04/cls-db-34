from django.urls import path
from .views import VerifyLicenseAPIView

app_name = 'api_licenses'

urlpatterns = [
    path('verify/', VerifyLicenseAPIView.as_view(), name='verify'),
]
