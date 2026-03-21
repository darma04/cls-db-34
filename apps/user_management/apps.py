"""
==========================================================================
 USER MANAGEMENT APPS - Konfigurasi Aplikasi Manajemen User
==========================================================================
 Modul untuk mengelola user (CRUD: tambah, lihat, edit, hapus).
 Menggunakan Profile dari auth module sebagai model utama.
 Tidak memiliki models sendiri — semua data ada di auth.Profile.
==========================================================================
"""
from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    """Konfigurasi aplikasi User Management — kelola akun pengguna."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_management'       # Path app
    verbose_name = 'User Management'    # Nama tampilan di admin
