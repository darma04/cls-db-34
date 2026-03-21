"""
==========================================================================
 DASHBOARD URLS - Routing URL untuk Dashboard ERP
==========================================================================
 app_name = 'dashboard' → Namespace URL
 Hanya 1 URL: /dashboard/ → DashboardView (halaman utama setelah login)
==========================================================================
"""

from django.urls import path
from .views import DashboardView

app_name = 'dashboard'  # Namespace URL

urlpatterns = [
    path('', DashboardView.as_view(), name='index'),
]
