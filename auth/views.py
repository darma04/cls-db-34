"""
==========================================================================
 AUTH VIEWS - Base View untuk Halaman Autentikasi
==========================================================================
 File ini berisi AuthView — base class (kelas dasar) untuk semua
 halaman autentikasi: Login, Register, Forgot Password, dll.

 Apa itu Base Class?
 - Kelas yang diwarisi (inherit) oleh kelas-kelas turunan
 - Berisi logika yang SAMA untuk semua halaman autentikasi
 - Mengurangi duplikasi kode (DRY principle)

 Kenapa halaman auth pakai layout khusus?
 - Halaman login/register tidak perlu sidebar dan navbar
 - Menggunakan 'layout_blank.html' → halaman kosong (full-screen form)
 - Berbeda dengan halaman dashboard yang pakai 'layout_vertical.html'

 Koneksi:
 - web_project/__init__.py → TemplateLayout.init() untuk inisialisasi
 - web_project/template_helpers/theme.py → TemplateHelper.set_layout()
 - auth/login/views.py → LoginView mewarisi AuthView
 - auth/register/views.py → RegisterView mewarisi AuthView
 - auth/forgot_password/views.py → ForgetPasswordView mewarisi AuthView
 - auth/reset_password/views.py → ResetPasswordView mewarisi AuthView
 - auth/verify_email/views.py → VerifyEmailView mewarisi AuthView
==========================================================================
"""

from django.views.generic import TemplateView                     # View generik untuk render template
from web_project import TemplateLayout                            # Engine layout proyek ini
from web_project.template_helpers.theme import TemplateHelper     # Helper untuk pengaturan tema


class AuthView(TemplateView):
    """
    Base view untuk semua halaman autentikasi.

    Mewarisi TemplateView dari Django — view yang hanya me-render template.
    Tidak ada form processing di sini (itu dilakukan di subclass masing-masing).

    Method yang di-override:
    - get_context_data() → Menambahkan layout_blank.html ke context

    Class turunan harus:
    - Menentukan template_name (di urls.py atau di class)
    - Mengimplementasikan get() dan post() sesuai kebutuhan
    """

    def get_context_data(self, **kwargs):
        """
        Menyiapkan context data untuk template.

        Langkah:
        1. Panggil TemplateLayout.init() → inisialisasi tema & layout
        2. Override layout_path ke 'layout_blank.html'
           → Layout tanpa sidebar, navbar, footer (cocok untuk auth pages)

        Parameter:
        - **kwargs: Keyword arguments dari parent class
          (yang diteruskan dari URL dispatcher)

        Return:
        - context: Dictionary yang berisi semua data untuk template
        """
        # Inisialisasi layout global (tema, sidebar, navbar, dll)
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))

        # Override layout ke blank (tanpa sidebar/navbar)
        # Semua halaman auth menggunakan layout kosong (full-screen)
        context.update(
            {
                "layout_path": TemplateHelper.set_layout("layout_blank.html", context),
            }
        )

        return context
