"""
==========================================================================
 WSGI CONFIG - Web Server Gateway Interface
==========================================================================
 File ini mengkonfigurasi WSGI (Web Server Gateway Interface) untuk proyek.

 Apa itu WSGI?
 - WSGI adalah standar Python untuk berkomunikasi antara web server
   (seperti Gunicorn, uWSGI, Apache mod_wsgi) dan aplikasi web Django.
 - WSGI digunakan untuk deployment PRODUKSI (bukan development).

 Cara kerja:
 1. Web server (Gunicorn) menerima HTTP request dari browser
 2. Request diteruskan ke WSGI application (variabel 'application')
 3. Django memproses request dan mengembalikan HTTP response
 4. Web server mengirim response kembali ke browser

 Kapan digunakan:
 - Saat deploy ke server produksi (misalnya: gunicorn config.wsgi:application)
 - TIDAK digunakan saat development (manage.py runserver sudah cukup)

 Koneksi:
 - config/settings.py → Konfigurasi Django yang dimuat
 - Gunicorn/uWSGI → Web server yang memanggil 'application'
 - requirements.txt → gunicorn==23.0.0 terdaftar sebagai dependensi

 Referensi:
 https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
==========================================================================
"""

import os  # Modul untuk mengatur variabel lingkungan

from django.core.wsgi import get_wsgi_application  # Fungsi untuk membuat WSGI app

# Atur settings module agar Django tahu konfigurasi mana yang dipakai
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Buat WSGI application object
# Object ini yang dipanggil oleh web server untuk setiap request
# Contoh penggunaan: gunicorn config.wsgi:application --bind 0.0.0.0:8000
application = get_wsgi_application()
