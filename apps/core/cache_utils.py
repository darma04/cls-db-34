"""
==========================================================================
 CORE CACHE UTILS - Utilitas Cache untuk Sistem Permission
==========================================================================
 File ini berisi utilitas caching untuk meningkatkan performa
 pengecekan permission.

 Apa itu Caching?
 - Menyimpan hasil query database di memori (RAM)
 - Request berikutnya mengambil dari CACHE (cepat), bukan dari DATABASE (lambat)
 - Contoh: has_permission() dipanggil 50x per request (setiap submenu di sidebar)
   → Tanpa cache: 50 query database
   → Dengan cache: 1 query + 49 cache hit

 Konsep:
 - Cache Key: Identitas unik data yang di-cache (contoh: 'user_perms_1_has_permission_read-produk')
 - Cache Timeout: Berapa lama data disimpan di cache (default: 5 menit)
 - Cache Invalidation: Menghapus cache saat data berubah

 Kapan cache HARUS di-invalidate?
 - Saat role user diubah
 - Saat permission role diupdate
 - Saat user dipindahkan ke role lain

 Koneksi:
 - django.core.cache → Backend cache (default: LocMemCache di settings.py)
 - apps/core/permissions.py → Bisa menggunakan decorator cache_user_permissions
 - auth/models.py → Profile (untuk mendapatkan user_id per role)
==========================================================================
"""

from django.core.cache import cache  # Framework cache bawaan Django
from functools import wraps          # Untuk decorator yang mempertahankan metadata


def cache_user_permissions(timeout=300):  # 300 detik = 5 menit
    """
    Decorator untuk meng-cache hasil pengecekan permission per user.
    Mengurangi jumlah query database secara SIGNIFIKAN.

    Parameter:
    - timeout: Berapa lama cache valid dalam detik (default: 300 = 5 menit)

    Cara pakai:
        @cache_user_permissions()
        def get_user_permissions(user):
            # Query database yang mahal
            ...

    Cara kerja:
    1. Buat cache key unik berdasarkan: user ID + nama fungsi + arguments
    2. Cek apakah hasil sudah ada di cache
    3. Jika ada (cache hit) → kembalikan langsung (tanpa query DB)
    4. Jika tidak ada (cache miss) → jalankan fungsi, simpan hasilnya di cache
    """
    def decorator(func):
        """Fungsi decorator — membungkus view function."""
        @wraps(func)  # Mempertahankan __name__ dan __doc__ dari fungsi asli
        def wrapper(user, *args, **kwargs):
            """Fungsi wrapper — logika pengecekan sebelum view dijalankan."""
            # User yang belum login → jangan cache
            if not user or not user.is_authenticated:
                return func(user, *args, **kwargs)

            # Buat cache key unik
            # Format: 'user_perms_{user_id}_{nama_fungsi}_{arg1-arg2-...}'
            # Contoh: 'user_perms_1_has_permission_read-produk-kategori'
            cache_key = f'user_perms_{user.id}_{func.__name__}_{"-".join(map(str, args))}'

            # Cek cache
            result = cache.get(cache_key)
            if result is not None:
                # Cache HIT → kembalikan langsung tanpa query
                return result

            # Cache MISS → jalankan fungsi dan simpan hasilnya
            result = func(user, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper
    return decorator


def invalidate_user_permissions_cache(user_id):
    """
    Menghapus semua cache permission untuk user tertentu.
    Harus dipanggil saat:
    - Role user diubah
    - User dipindahkan ke role lain

    Cara kerja:
    - Menggunakan pendekatan "version number"
    - Setiap user punya nomor versi cache
    - Saat di-invalidate → versi naik → cache key lama tidak valid lagi

    Kenapa tidak hapus langsung?
    - Django cache (LocMemCache) tidak mendukung penghapusan berdasarkan pattern
    - Contoh: tidak bisa hapus semua key yang dimulai dengan 'user_perms_1_*'
    - Jadi kita gunakan version number sebagai workaround
    """
    cache_version_key = f'user_perms_version_{user_id}'
    current_version = cache.get(cache_version_key, 0)
    cache.set(cache_version_key, current_version + 1)


def invalidate_role_permissions_cache(role_code):
    """
    Menghapus cache permission untuk SEMUA user yang punya role tertentu.
    Harus dipanggil saat:
    - Permission role diupdate (contoh: ADMIN sekarang bisa akses modul baru)

    Alur:
    1. Cari semua user yang punya role ini (dari Profile.role)
    2. Invalidate cache masing-masing user

    Parameter:
    - role_code: Kode role (contoh: 'ADMIN', 'KASIR')
    """
    from auth.models import Profile
    from django.contrib.auth.models import User

    # Cari semua user_id yang punya role ini
    user_ids = Profile.objects.filter(role=role_code).values_list('user_id', flat=True)

    # Invalidate cache untuk setiap user
    for user_id in user_ids:
        invalidate_user_permissions_cache(user_id)
