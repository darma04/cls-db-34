"""
==========================================================================
 PAGES APPS - Konfigurasi Aplikasi Pages (Halaman Statis)
==========================================================================
 Modul pages menangani halaman-halaman statis seperti error, maintenance,
 coming soon, dan not authorized. Tidak memiliki models atau signals.
==========================================================================
"""
from django.apps import AppConfig


class PagesConfig(AppConfig):
    """Konfigurasi aplikasi Pages — halaman statis dan error."""
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.pages"  # Path app (harus sesuai INSTALLED_APPS)
