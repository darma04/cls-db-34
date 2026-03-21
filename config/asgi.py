"""
==========================================================================
 ASGI CONFIG - Asynchronous Server Gateway Interface
==========================================================================
 File ini mengkonfigurasi ASGI (Asynchronous Server Gateway Interface).

 Apa itu ASGI?
 - ASGI adalah versi asinkron dari WSGI.
 - Mendukung protokol WebSocket, HTTP/2, dan long-polling.
 - Digunakan jika aplikasi membutuhkan fitur real-time/async.

 Perbedaan WSGI vs ASGI:
 - WSGI: Sinkron (1 request = 1 thread, menunggu selesai baru proses berikutnya)
 - ASGI: Asinkron (bisa memproses banyak request bersamaan tanpa blocking)

 Kapan digunakan:
 - Jika butuh WebSocket (contoh: chat real-time, notifikasi live)
 - Jika butuh async views di Django
 - Deploy dengan Daphne atau Uvicorn sebagai pengganti Gunicorn

 Koneksi:
 - config/settings.py → Konfigurasi Django yang dimuat
 - Daphne/Uvicorn → Server ASGI yang memanggil 'application'

 Referensi:
 https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
==========================================================================
"""

import os  # Modul untuk mengatur variabel lingkungan

from django.core.asgi import get_asgi_application  # Fungsi untuk membuat ASGI app

# Atur settings module agar Django tahu konfigurasi mana yang dipakai
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Buat ASGI application object
# Object ini dipanggil oleh server ASGI untuk setiap request
# Contoh: uvicorn config.asgi:application --host 0.0.0.0 --port 8000
application = get_asgi_application()
