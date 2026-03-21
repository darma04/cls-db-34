"""
==========================================================================
 USER MANAGEMENT APP - Modul Manajemen User
==========================================================================
 Package ini menangani pengelolaan akun user di sistem ERP.

 Berisi:
 - views.py  → CRUD user (tambah, edit, hapus, detail)
 - models.py → Model tambahan jika ada (atau menggunakan auth.User)
 - urls.py   → Routing URL manajemen user

 Fitur:
 - Daftar user dengan filter (role, status aktif, pencarian)
 - Tambah user baru (set password + assign role)
 - Edit user (ubah username, role, status aktif/nonaktif)
 - Detail user (lihat role, permission, riwayat login)
 - Hapus user (soft delete / hard delete)
 - AJAX detail user untuk modal popup

 Terhubung dengan:
 - django.contrib.auth.models.User → Model user bawaan Django
 - auth/models.py → Profile (role, avatar, data tambahan)
 - apps/core/models.py → RolePermission (dynamic roles)
 - apps/core/mixins.py → Permission mixins untuk proteksi akses
==========================================================================
"""
from django.apps import AppConfig


class UserManagementConfig(AppConfig):
    """
    Konfigurasi aplikasi User Management.

    Atribut:
    - default_auto_field: Tipe ID default (BigAutoField = 64-bit integer)
    - name: Path lengkap app
    - verbose_name: Nama tampilan di Django Admin
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.user_management'
    verbose_name = 'User Management'
