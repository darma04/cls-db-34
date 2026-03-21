"""
==========================================================================
 AUTH HELPERS - Fungsi Bantuan untuk Email
==========================================================================
 File ini berisi fungsi-fungsi helper (pembantu) untuk mengirim email:
 - send_email() → Fungsi dasar kirim email via SMTP
 - send_verification_email() → Kirim email verifikasi saat registrasi
 - send_password_reset_email() → Kirim email reset password

 Mengapa pengaturan SMTP disimpan di database?
 - Agar admin bisa mengubah konfigurasi email tanpa edit kode
 - Menggunakan model PengaturanPerusahaan (singleton, pk=1)
 - Admin bisa mengatur: SMTP host, port, username, password, TLS

 Koneksi:
 - apps/pengaturan/models.py → PengaturanPerusahaan (konfigurasi SMTP)
 - auth/register/views.py → Memanggil send_verification_email()
 - auth/forgot_password/views.py → Memanggil send_password_reset_email()
 - auth/verify_email/views.py → Memanggil send_verification_email()
 - django.core.mail → Framework email bawaan Django
==========================================================================
"""

from django.core.mail import EmailMessage  # Class untuk membuat dan mengirim email
from django.urls import reverse            # Fungsi untuk mengubah nama URL menjadi path URL
from django.conf import settings           # Akses pengaturan Django
import logging                             # Modul logging standar Python

# Inisialisasi logger untuk modul auth helpers
logger = logging.getLogger(__name__)


def send_email(subject, email, message):
    """
    Fungsi dasar untuk mengirim email menggunakan pengaturan SMTP dari database.

    Parameter:
    - subject: Judul/subjek email (contoh: "Verifikasi Email Anda")
    - email: Alamat email tujuan (contoh: "user@example.com")
    - message: Isi pesan email (bisa HTML atau plain text)

    Return: True jika berhasil, False jika gagal

    Cara kerja:
    1. Load pengaturan SMTP dari PengaturanPerusahaan (singleton)
    2. Cek apakah SMTP sudah dikonfigurasi (username & password)
    3. Buat koneksi SMTP dengan get_connection()
    4. Buat EmailMessage dan kirim via koneksi tersebut

    Kenapa tidak pakai settings.py langsung?
    - Agar admin bisa mengubah konfigurasi SMTP dari admin panel
    - Tanpa perlu restart server atau edit file kode
    """
    try:
        # Import di dalam fungsi (lazy import) untuk menghindari circular import
        # Circular import: A import B, B import A → error
        from apps.pengaturan.models import PengaturanPerusahaan
        pengaturan = PengaturanPerusahaan.load()  # Load singleton (pk=1)

        # Validasi: apakah SMTP sudah dikonfigurasi?
        if not pengaturan.email_smtp_user or not pengaturan.email_smtp_password:
            logger.warning("Pengaturan email SMTP belum dikonfigurasi di Pengaturan Perusahaan")
            return False

        # Buat koneksi SMTP manual (bukan dari settings.py)
        # Ini memungkinkan konfigurasi diambil dari database runtime
        from django.core.mail import get_connection
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',  # Backend email SMTP
            host=pengaturan.email_smtp_host,          # Host SMTP (contoh: smtp.gmail.com)
            port=pengaturan.email_smtp_port,          # Port SMTP (contoh: 587 untuk TLS)
            username=pengaturan.email_smtp_user,      # Username SMTP (email pengirim)
            password=pengaturan.email_smtp_password,  # Password SMTP atau App Password
            use_tls=pengaturan.email_use_tls,         # True jika pakai TLS (port 587)
        )

        # Buat dan kirim email
        email_from = pengaturan.email_smtp_user   # Alamat pengirim
        recipient_list = [email]                   # Daftar penerima (bisa lebih dari 1)
        email_msg = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
        email_msg.send()                          # Kirim email
        return True

    except Exception as e:
        # Jika terjadi error (koneksi gagal, SMTP salah, dll)
        logger.error("Gagal mengirim email: %s", e, exc_info=True)
        return False


def get_absolute_url(path):
    """
    Membuat URL lengkap dengan domain.

    Parameter:
    - path: Path relatif (contoh: '/verify/email/abc-123/')

    Return: URL lengkap (contoh: 'http://localhost:8000/verify/email/abc-123/')

    Kenapa dibutuhkan:
    - Link di email harus URL lengkap (bukan relatif)
    - BASE_URL diambil dari settings.py
    """
    return settings.BASE_URL + path


def send_verification_email(email, token):
    """
    Mengirim email verifikasi ke user baru setelah registrasi.

    Parameter:
    - email: Email tujuan (contoh: "user@example.com")
    - token: UUID token verifikasi (contoh: "a1b2c3d4-...")

    Alur kerja:
    1. Load template email dari PengaturanPerusahaan
    2. Buat URL verifikasi: http://domain/verify/email/{token}/
    3. Ganti placeholder {verification_link} di template
    4. Gabungkan: header + body + footer
    5. Ganti placeholder umum: {company_name}, {user_email}
    6. Kirim email via send_email()

    Koneksi:
    - PengaturanPerusahaan.register_subject → Subjek email
    - PengaturanPerusahaan.register_message → Body template
    - PengaturanPerusahaan.email_header → Header email
    - PengaturanPerusahaan.email_footer → Footer email
    """
    from apps.pengaturan.models import PengaturanPerusahaan
    pengaturan = PengaturanPerusahaan.load()

    # Ambil subjek dari template yang disimpan di database
    subject = pengaturan.register_subject

    # Buat URL verifikasi lengkap
    # reverse('verify-email', ...) → '/verify/email/abc-123/'
    # get_absolute_url() → 'http://localhost:8000/verify/email/abc-123/'
    verification_url = get_absolute_url(reverse('verify-email', kwargs={'token': token}))

    # Ganti placeholder {verification_link} di template body
    message_body = pengaturan.register_message.replace('{verification_link}', verification_url)

    # Gabungkan: header + body + footer → pesan email lengkap
    full_message = f"{pengaturan.email_header}\n\n{message_body}\n\n{pengaturan.email_footer}"

    # Ganti placeholder umum di seluruh pesan
    full_message = full_message.replace('{company_name}', pengaturan.nama_perusahaan)
    full_message = full_message.replace('{user_email}', email)

    # Kirim email
    send_email(subject, email, full_message)


def send_password_reset_email(email, token):
    """
    Mengirim email reset password ke user yang lupa password.

    Parameter:
    - email: Email tujuan
    - token: UUID token reset password

    Alur kerja sama seperti send_verification_email(),
    tapi menggunakan template forgot_password dari PengaturanPerusahaan.

    Koneksi:
    - PengaturanPerusahaan.forgot_password_subject → Subjek email
    - PengaturanPerusahaan.forgot_password_message → Body template
    """
    from apps.pengaturan.models import PengaturanPerusahaan
    pengaturan = PengaturanPerusahaan.load()

    # Ambil subjek dari template reset password
    subject = pengaturan.forgot_password_subject

    # Buat URL reset password lengkap
    reset_url = get_absolute_url(reverse('reset-password', kwargs={'token': token}))

    # Ganti placeholder {reset_link}
    message_body = pengaturan.forgot_password_message.replace('{reset_link}', reset_url)

    # Gabungkan header + body + footer
    full_message = f"{pengaturan.email_header}\n\n{message_body}\n\n{pengaturan.email_footer}"

    # Ganti placeholder umum
    full_message = full_message.replace('{company_name}', pengaturan.nama_perusahaan)
    full_message = full_message.replace('{user_email}', email)

    # Kirim email
    send_email(subject, email, full_message)
