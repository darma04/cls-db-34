"""
==========================================================================
 CORE APP - Modul Inti Sistem Permission & Keamanan
==========================================================================
 Package ini adalah JANTUNG sistem keamanan ERP.

 Berisi:
 - models.py       → Model RolePermission (RBAC database-driven)
 - permissions.py  → Fungsi has_permission(), get_user_role(), dll
 - mixins.py       → Mixin permission untuk Class-Based Views
 - context_processors.py → Menyuntikkan permission ke template
 - cache_utils.py  → Utilitas caching untuk performa permission
 - templatetags/   → Custom template tags untuk pengecekan permission

 Semua modul lain BERGANTUNG pada package ini untuk:
 - Mengecek hak akses user sebelum menampilkan halaman
 - Memfilter menu sidebar berdasarkan permission
 - Membatasi aksi CRUD berdasarkan role
==========================================================================
"""
