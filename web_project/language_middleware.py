"""
==========================================================================
 LANGUAGE MIDDLEWARE - Middleware Bahasa Default
==========================================================================
 File ini berisi middleware kustom untuk mengatur bahasa default aplikasi.

 Apa itu Middleware?
 - Middleware adalah "lapisan" kode yang dijalankan di SETIAP request dan response.
 - Setiap request dari browser melewati semua middleware secara berurutan.
 - Middleware bisa memodifikasi request sebelum sampai ke view,
   atau memodifikasi response sebelum dikirim ke browser.

 Urutan middleware di settings.py:
 Request → SecurityMiddleware → GZipMiddleware → WhiteNoiseMiddleware
         → SessionMiddleware → LocaleMiddleware → DefaultLanguageMiddleware (INI)
         → CommonMiddleware → CsrfViewMiddleware → AuthenticationMiddleware
         → MessageMiddleware → XFrameOptionsMiddleware → ActivityLogMiddleware
         → View → Response (urutan terbalik)

 Cara kerja middleware ini:
 1. Cek apakah cookie 'django_language' sudah ada di browser user
 2. Jika BELUM ada → set bahasa default dari settings.LANGUAGE_CODE
 3. Jika SUDAH ada → biarkan (user sudah memilih bahasa sebelumnya)

 Koneksi:
 - config/settings.py → MIDDLEWARE list (tempat middleware ini didaftarkan)
 - config/settings.py → LANGUAGE_CODE (bahasa default yang digunakan)
 - django.utils.translation → Modul Django untuk aktivasi bahasa
==========================================================================
"""

from django.conf import settings               # Mengakses pengaturan Django
from django.utils.translation import activate   # Fungsi untuk mengaktifkan bahasa


class DefaultLanguageMiddleware:
    """
    Middleware untuk mengatur bahasa default berdasarkan settings.LANGUAGE_CODE.

    Middleware ini memastikan setiap user baru mendapatkan bahasa default
    yang sudah dikonfigurasi (misal: 'id' untuk Bahasa Indonesia).

    Pola Middleware Django:
    - __init__(get_response): Dipanggil SEKALI saat server start
    - __call__(request): Dipanggil untuk SETIAP request
    """

    def __init__(self, get_response):
        """
        Konstruktor middleware — dipanggil SEKALI saat Django start.

        Parameter:
        - get_response: Fungsi/middleware berikutnya dalam rantai
          Harus disimpan dan dipanggil di __call__()
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Proses setiap request — dipanggil untuk SETIAP HTTP request.

        Alur:
        1. Cek cookie 'django_language' di browser user
        2. Jika belum ada → aktifkan bahasa default dan set cookie
        3. Jika sudah ada → lanjutkan tanpa perubahan
        4. Lanjutkan ke middleware/view berikutnya via self.get_response()
        """
        # Cek apakah cookie bahasa belum di-set di browser user
        if 'django_language' not in request.COOKIES:
            # Ambil bahasa default dari settings.py (misal: 'id')
            default_language = settings.LANGUAGE_CODE

            # Aktifkan bahasa tersebut untuk request ini
            # Ini mempengaruhi semua terjemahan Django ({% trans %}, gettext, dll)
            activate(default_language)

            # Proses request ke middleware/view berikutnya
            response = self.get_response(request)

            # Set cookie 'django_language' di browser agar tidak perlu set ulang
            response.set_cookie('django_language', default_language)
        else:
            # Cookie sudah ada → user sudah punya preferensi bahasa
            # Langsung proses request tanpa mengubah bahasa
            response = self.get_response(request)

        return response
