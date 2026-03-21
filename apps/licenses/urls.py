"""
==========================================================================
 LICENSES API URLS — Routing REST API Lisensi
==========================================================================
 Base URL: /api/v1/license/
 Endpoints:
 - POST /api/v1/license/activate/       → Aktivasi + bind hardware
 - POST /api/v1/license/validate/       → Pengecekan berkala
 - POST /api/v1/license/deactivate/     → Unlink device
 - GET  /api/v1/license/status/<key>/   → Cek status (read-only)
==========================================================================
"""
from django.urls import path
from .views import license_activate, license_validate, license_deactivate, license_status

app_name = 'licenses'

urlpatterns = [
    path('license/activate/', license_activate, name='license_activate'),
    path('license/validate/', license_validate, name='license_validate'),
    path('license/deactivate/', license_deactivate, name='license_deactivate'),
    path('license/status/<str:key>/', license_status, name='license_status'),
]
