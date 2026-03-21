"""
==========================================================================
 DASHBOARD APPS - Konfigurasi aplikasi Django untuk Dashboard
==========================================================================
"""
from django.apps import AppConfig

class DashboardConfig(AppConfig):
    """Konfigurasi aplikasi Dashboard (halaman utama ERP)."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.dashboard'
    verbose_name = 'Dashboard'
