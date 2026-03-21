"""
==========================================================================
 CORE ADMIN - Registrasi RolePermission ke Django Admin
==========================================================================
 Mendaftarkan model RolePermission ke panel Django Admin (/admin/).
 Menggunakan ModelAdmin dengan kustomisasi:
 - list_display: Kolom yang ditampilkan di daftar
 - list_filter: Filter sidebar berdasarkan role/module
 - search_fields: Pencarian berdasarkan role/module/description
 - fieldsets: Pengelompokan field dalam form edit

 Terhubung dengan:
 - core/models.py → RolePermission (model permission RBAC)
==========================================================================
"""
from django.contrib import admin       # Framework admin bawaan Django
from .models import RolePermission     # Model permission RBAC (Role-Based Access Control)


# Mendaftarkan RolePermission ke panel admin dengan kustomisasi lengkap
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    """
    Admin untuk model RolePermission (hak akses per role dan modul).

    Kustomisasi:
    - list_display: Menampilkan semua permission flags (can_view, can_create, dll)
    - fieldsets: Mengelompokkan field dalam form edit menjadi beberapa bagian
    - readonly_fields: Field yang tidak bisa diedit (timestamp)
    """
    # Kolom yang ditampilkan di tabel list
    # Contoh tampilan:
    # | role      | module  | can_view | can_create | can_edit | can_delete | updated_at |
    # | admin     | produk  | ✓        | ✓          | ✓        | ✓          | 2024-01-15 |
    # | staff     | produk  | ✓        | ✗          | ✗        | ✗          | 2024-01-15 |
    list_display = ['role', 'module', 'can_view', 'can_create', 'can_edit', 'can_delete', 'updated_at']

    # Filter sidebar — bisa filter berdasarkan role atau module
    list_filter = ['role', 'module']

    # Search box — mencari berdasarkan nama role, module, atau deskripsi
    search_fields = ['role', 'module', 'description']

    # Field yang hanya bisa dibaca (tidak bisa diedit di form)
    readonly_fields = ['created_at', 'updated_at']

    # Fieldsets: Mengelompokkan field dalam form edit menjadi beberapa bagian
    # Ini membuat form lebih rapi dan mudah dipahami
    fieldsets = (
        # Bagian 1: Informasi role dan module
        ('Role & Module', {
            'fields': ('role', 'module')
        }),
        # Bagian 2: Checkbox permission (can_view, can_create, can_edit, can_delete)
        ('Permissions', {
            'fields': ('can_view', 'can_create', 'can_edit', 'can_delete')
        }),
        # Bagian 3: Info tambahan (collapse = bisa di-hide/show)
        # 'classes': ('collapse',) membuat bagian ini terlipat secara default
        ('Additional Info', {
            'fields': ('description', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # Terlipat default, klik untuk buka
        }),
    )
