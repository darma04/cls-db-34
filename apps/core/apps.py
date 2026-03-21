"""
==========================================================================
 CORE APPS - Konfigurasi Aplikasi Core
==========================================================================
 File ini mengkonfigurasi aplikasi 'apps.core' sebagai Django App.

 Core adalah modul INTI yang berisi:
 - RolePermission model (RBAC)
 - Permission checking functions
 - Permission mixins untuk views
 - Context processors untuk template
 - Cache utilities

 Koneksi:
 - config/settings.py → INSTALLED_APPS: "apps.core"
 - Semua apps lain → Menggunakan mixin dan permission dari core
==========================================================================
"""

from django.apps import AppConfig  # Base class untuk konfigurasi app


class CoreConfig(AppConfig):
    """
    Konfigurasi aplikasi Core.

    Atribut:
    - default_auto_field: Tipe field ID otomatis (BigAutoField = integer 64-bit)
    - name: Nama modul Python lengkap (harus 'apps.core' karena ada di subfolder apps/)
    - verbose_name: Nama yang ditampilkan di admin panel
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.core'   # Path modul Python (folder apps/core/)
    verbose_name = 'Core'  # Nama yang ditampilkan di Django admin
