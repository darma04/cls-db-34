"""
==========================================================================
 AUTH ADMIN - Konfigurasi Admin Panel untuk Model Profile
==========================================================================
 File ini mendaftarkan model Profile ke Django Admin panel.
 Django Admin adalah interface bawaan Django untuk mengelola data
 database melalui browser di URL /admin/.

 Koneksi:
 - auth/models.py → Model Profile yang didaftarkan di sini
 - Django Admin (django.contrib.admin) → Framework admin bawaan
==========================================================================
"""

from django.contrib import admin  # Modul admin bawaan Django
from .models import Profile       # Import model Profile dari file models.py di folder yang sama


class Member(admin.ModelAdmin):
    """
    Konfigurasi tampilan model Profile di halaman admin Django.

    list_display: Kolom-kolom yang ditampilkan di tabel daftar Profile.
    Setiap string harus sesuai dengan nama field di model Profile.

    Kenapa pakai admin.ModelAdmin?
    - Menyesuaikan tampilan default admin Django
    - Bisa menambahkan filter, search, dll di kemudian hari
    """
    list_display = (
        "user",          # Kolom: username dari relasi OneToOneField ke User
        "email",         # Kolom: alamat email profile
        "is_verified",   # Kolom: status verifikasi email (True/False)
        "created_at",    # Kolom: tanggal pembuatan profile (field dibuat_pada)
    )


# Mendaftarkan model Profile dengan konfigurasi Member ke admin site
# Setelah ini, Profile bisa dikelola di http://localhost:8000/admin/
admin.site.register(Profile, Member)
