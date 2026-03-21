#!/usr/bin/env python
"""
==========================================================================
 MANAGE.PY - Entry Point Utama Django
==========================================================================
 File ini adalah titik masuk (entry point) untuk menjalankan semua
 perintah manajemen Django melalui terminal/command line.

 Perintah yang sering digunakan:
 - python manage.py runserver        → Jalankan server development
 - python manage.py makemigrations   → Buat file migrasi database
 - python manage.py migrate          → Jalankan migrasi ke database
 - python manage.py createsuperuser  → Buat akun admin/superuser
 - python manage.py shell            → Buka Python shell interaktif
 - python manage.py collectstatic    → Kumpulkan file statis untuk produksi
 - python manage.py check            → Cek error konfigurasi proyek

 Cara kerja:
 1. Set variabel environment DJANGO_SETTINGS_MODULE ke 'config.settings'
 2. Panggil execute_from_command_line() dari Django
 3. Django membaca settings.py dan menjalankan perintah yang diminta

 Koneksi:
 - config/settings.py → File konfigurasi yang dimuat saat Django start
 - Django Management Framework → Framework perintah bawaan Django
==========================================================================
"""

import os   # Modul untuk mengakses variabel lingkungan (environment variables)
import sys  # Modul untuk mengakses argumen command line (sys.argv)


def main():
    """
    Fungsi utama yang dijalankan saat file ini dieksekusi.

    Langkah-langkah:
    1. Mengatur DJANGO_SETTINGS_MODULE → memberitahu Django dimana file settings berada
    2. Mengimpor dan menjalankan execute_from_command_line() dari Django
    3. Fungsi ini membaca argumen dari terminal (contoh: 'runserver', 'migrate')
       dan menjalankan perintah yang sesuai
    """
    # Atur variabel lingkungan agar Django tahu menggunakan config/settings.py
    # setdefault() artinya: set nilai hanya jika belum ada sebelumnya
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        # Import fungsi execute_from_command_line dari Django
        # Fungsi ini yang memproses semua perintah Django (runserver, migrate, dll)
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Jika Django tidak terinstall atau virtual environment tidak aktif,
        # tampilkan pesan error yang jelas
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Jalankan perintah Django berdasarkan argumen dari terminal
    # sys.argv berisi: ['manage.py', 'runserver'] atau ['manage.py', 'migrate'] dll
    execute_from_command_line(sys.argv)


# Blok ini memastikan fungsi main() hanya dijalankan jika file ini
# dieksekusi langsung (bukan saat diimport oleh file lain)
if __name__ == "__main__":
    main()
