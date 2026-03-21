"""
==========================================================================
 AUTH URLS - Routing URL untuk Modul Autentikasi
==========================================================================
 File ini mendefinisikan semua URL pattern untuk fitur autentikasi:
 login, logout, register, verifikasi email, lupa password, reset password.

 Apa itu URL Pattern?
 - Pemetaan antara URL di browser dengan view (controller) Python
 - Contoh: URL '/login/' → dipetakan ke LoginView

 Kenapa URL didefinisikan di sini (bukan di config/urls.py)?
 - Prinsip modularitas: setiap app punya url sendiri
 - Di config/urls.py, cukup include: path("", include("auth.urls"))
 - Lebih mudah dikelola saat proyek membesar

 Koneksi:
 - config/urls.py → include("auth.urls") untuk memuat URL ini
 - auth/login/views.py → LoginView
 - auth/register/views.py → RegisterView
 - auth/forgot_password/views.py → ForgetPasswordView
 - auth/reset_password/views.py → ResetPasswordView
 - auth/verify_email/views.py → VerifyEmailTokenView, VerifyEmailView
 - templates/auth/ → Template HTML untuk setiap halaman
 - django.contrib.auth.views.LogoutView → View logout bawaan Django
==========================================================================
"""

from django.urls import path                        # Fungsi untuk membuat URL pattern
from django.contrib.auth.views import LogoutView    # View logout bawaan Django (sudah jadi)
from .register.views import RegisterView            # View register dari subfolder
from .login.views import LoginView                  # View login dari subfolder
from .forgot_password.views import ForgetPasswordView    # View lupa password
from .reset_password.views import ResetPasswordView      # View reset password
from .verify_email.views import VerifyEmailTokenView, VerifyEmailView, SendVerificationView  # View verifikasi email


# ==================== DAFTAR URL AUTENTIKASI ====================
# Setiap path() menerima:
#   1. URL string (contoh: "login/")
#   2. View class.as_view() dengan optional template_name
#   3. name= untuk referensi di template/redirect (contoh: redirect("login"))
urlpatterns = [
    # ---------- LOGIN ----------
    # URL: /login/
    # Template: templates/auth/login.html
    # Name: 'login' → dipakai untuk redirect dan {% url 'login' %}
    path(
        "login/",
        LoginView.as_view(template_name="auth/login.html"),
        name="login",
    ),

    # ---------- LOGOUT ----------
    # URL: /logout/
    # Menggunakan LogoutView bawaan Django (tidak perlu custom view)
    # Otomatis menghapus session dan redirect ke LOGIN_URL
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # ---------- REGISTRASI ----------
    # URL: /register/
    # Template: templates/auth/register.html
    path(
        "register/",
        RegisterView.as_view(template_name="auth/register.html"),
        name="register",
    ),

    # ---------- VERIFIKASI EMAIL (Halaman informasi) ----------
    # URL: /verify_email/
    # Halaman yang menampilkan pesan "Cek email Anda untuk verifikasi"
    path(
        "verify_email/",
        VerifyEmailView.as_view(template_name="auth/verify_email.html"),
        name="verify-email-page",
    ),

    # ---------- VERIFIKASI EMAIL (Proses token) ----------
    # URL: /verify/email/{token}/
    # Dipanggil saat user klik link verifikasi di email
    # <str:token>: Parameter dinamis berisi UUID token
    path(
        "verify/email/<str:token>/",
        VerifyEmailTokenView.as_view(),
        name="verify-email",
    ),

    # ---------- KIRIM ULANG VERIFIKASI ----------
    # URL: /send_verification/
    # Mengirim ulang email verifikasi ke user
    path(
        "send_verification/",
        SendVerificationView.as_view(),
        name="send-verification",
    ),

    # ---------- LUPA PASSWORD ----------
    # URL: /forgot_password/
    # Form untuk memasukkan email dan request link reset password
    path(
        "forgot_password/",
        ForgetPasswordView.as_view(template_name="auth/forgot_password.html"),
        name="forgot-password",
    ),

    # ---------- RESET PASSWORD ----------
    # URL: /reset_password/{token}/
    # Form untuk memasukkan password baru
    # <str:token>: UUID token dari email reset password
    path(
        "reset_password/<str:token>/",
        ResetPasswordView.as_view(template_name="auth/reset_password.html"),
        name="reset-password",
    ),

]
