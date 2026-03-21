"""
==========================================================================
 TEMPLATE CONFIG - Konfigurasi Tema & Layout Template
==========================================================================
 File ini mengatur tampilan visual aplikasi — tema, layout, navbar, dll.
 Diimpor oleh config/settings.py dan digunakan oleh TemplateHelper.

 Konfigurasi:
 - TEMPLATE_CONFIG → Layout (vertical/horizontal), tema, style (light/dark)
 - THEME_VARIABLES → Metadata template (nama, versi, URL)
 - THEME_LAYOUT_DIR → Direktori file layout template

 Catatan: Ubah nilai di TEMPLATE_CONFIG untuk mengubah tampilan
 aplikasi tanpa perlu mengubah kode HTML.

 Terhubung dengan:
 - config/settings.py → Mengimpor TEMPLATE_CONFIG, THEME_VARIABLES, THEME_LAYOUT_DIR
 - web_project/template_helpers/theme.py → TemplateHelper membaca TEMPLATE_CONFIG
 - web_project/__init__.py → TemplateLayout menggunakan konfigurasi ini
 - templates/layout/ → File layout HTML yang dipengaruhi konfigurasi ini
==========================================================================
"""

# ╔══════════════════════════════════════════════════════════════╗
# ║           KONFIGURASI TEMPLATE (TEMPLATE_CONFIG)            ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Dictionary ini mengontrol SELURUH tampilan visual aplikasi.
# Ubah nilai di sini untuk mengubah tampilan tanpa edit kode HTML.
#
# Cara kerja:
# 1. settings.py mengimpor file ini
# 2. TemplateHelper.init_context() membaca TEMPLATE_CONFIG
# 3. TemplateHelper.map_context() mengkonversi nilai ke CSS class
# 4. CSS class dikirim ke template HTML untuk rendering
#

TEMPLATE_CONFIG = {
    # ===== LAYOUT =====
    # Tipe layout navigasi menu utama
    # "vertical"   → Menu sidebar di sisi kiri (default, cocok untuk desktop)
    # "horizontal" → Menu bar di bagian atas (cocok untuk sedikit menu)
    "layout": "vertical",

    # ===== TEMA =====
    # Tema warna keseluruhan aplikasi
    # "theme-default"   → Tema standar (sidebar gelap, konten terang)
    # "theme-bordered"  → Tema dengan border/garis pemisah
    # "theme-semi-dark" → Tema semi-gelap (sidebar sangat gelap)
    "theme": "theme-default",

    # ===== GAYA WARNA =====
    # Mode warna tampilan (light/dark mode)
    # "light"  → Mode terang (latar belakang putih) — default
    # "dark"   → Mode gelap (latar belakang hitam/abu-abu)
    # "system" → Otomatis ikut pengaturan OS user
    "style": "light",

    # ===== RTL (Right-to-Left) =====
    # Dukungan untuk bahasa RTL (Arab, Ibrani, dll)
    # True  → Aktifkan dukungan RTL (file CSS RTL dimuat)
    # False → Nonaktifkan dukungan RTL
    "rtl_support": True,

    # Mode RTL — apakah layout dibalik ke kanan-ke-kiri
    # True  → Aktifkan mode RTL (teks dan layout dari kanan ke kiri)
    # False → Mode LTR normal (kiri ke kanan) — default
    # Catatan: rtl_support harus True agar rtl_mode bisa aktif
    "rtl_mode": False,

    # ===== CUSTOMIZER =====
    # Panel pengaturan tema yang muncul di sisi kanan layar
    # Memungkinkan user mengubah tema secara live (tanpa edit kode)

    # has_customizer: Apakah file JS customizer dimuat?
    # True  → File JS dimuat, pengaturan bisa disimpan di localStorage
    # False → File JS TIDAK dimuat, localStorage tidak berfungsi
    "has_customizer": True,

    # display_customizer: Apakah tombol customizer ditampilkan di UI?
    # True  → Tombol gear/roda gigi muncul di kanan layar
    # False → Tombol disembunyikan, tapi JS tetap dimuat (localStorage tetap jalan)
    "display_customizer": True,

    # ===== LAYOUT KONTEN =====
    # Lebar area konten utama
    # "compact" → Lebar terbatas (container-xxl, max ~1400px) — lebih rapi
    # "wide"    → Lebar penuh (container-fluid, 100% layar) — lebih luas
    "content_layout": "compact",

    # ===== NAVBAR (Menu Atas) =====
    # Perilaku navbar di bagian atas halaman
    # "fixed"  → Navbar tetap di atas saat scroll (selalu terlihat)
    # "static" → Navbar ikut scroll (hilang saat scroll ke bawah)
    # "hidden" → Navbar disembunyikan sepenuhnya
    # Catatan: Hanya berlaku untuk layout "vertical"
    "navbar_type": "fixed",

    # ===== HEADER (Layout Horizontal) =====
    # Perilaku header menu di layout horizontal
    # "fixed"  → Header tetap di atas saat scroll
    # "static" → Header ikut scroll
    # Catatan: Hanya berlaku untuk layout "horizontal"
    "header_type": "fixed",

    # ===== MENU SIDEBAR =====
    # menu_fixed: Apakah sidebar menu tetap saat scroll?
    # True  → Sidebar tetap di posisi (fixed) — selalu terlihat
    # False → Sidebar ikut scroll halaman
    # Catatan: Hanya berlaku untuk layout "vertical"
    "menu_fixed": True,

    # menu_collapsed: Apakah sidebar dalam keadaan collapse (sempit)?
    # True  → Sidebar sempit (hanya ikon, tanpa teks) — hemat ruang
    # False → Sidebar penuh (ikon + teks) — default
    # Catatan: Hanya berlaku untuk layout "vertical"
    "menu_collapsed": False,

    # ===== FOOTER =====
    # footer_fixed: Apakah footer tetap di bawah layar?
    # True  → Footer selalu terlihat di bawah (fixed)
    # False → Footer ada di akhir konten (default)
    "footer_fixed": False,

    # ===== DROPDOWN HOVER (Layout Horizontal) =====
    # Apakah dropdown menu terbuka saat mouse hover?
    # True  → Dropdown terbuka saat hover (tanpa klik)
    # False → Dropdown terbuka hanya saat diklik
    # Catatan: Hanya berlaku untuk layout "horizontal"
    "show_dropdown_onhover": True,

    # ===== KONTROL CUSTOMIZER =====
    # Daftar opsi yang ditampilkan di panel customizer
    # Hapus item dari list untuk menyembunyikan opsi tersebut dari user
    "customizer_controls": [
        "rtl",                  # Toggle RTL mode
        "style",                # Pilihan light/dark/system
        "headerType",           # Pilihan header fixed/static
        "contentLayout",        # Pilihan compact/wide
        "layoutCollapsed",      # Toggle sidebar collapse
        "showDropdownOnHover",  # Toggle dropdown hover
        "layoutNavbarOptions",  # Pilihan navbar fixed/static/hidden
        "themes",               # Pilihan tema warna
    ],
}


# ╔══════════════════════════════════════════════════════════════╗
# ║           VARIABEL TEMA (THEME_VARIABLES)                   ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Metadata dan informasi branding template.
# Digunakan di template HTML untuk menampilkan:
# - Nama aplikasi di title bar dan sidebar
# - Versi aplikasi
# - Link media sosial di footer
# - Informasi lisensi dan dokumentasi
#
# Diakses via: TemplateHelper.get_theme_variables('key')
#

THEME_VARIABLES = {
    # Informasi pembuat/developer
    "creator_name": "SERPTECH",                          # Nama tim/perusahaan pembuat
    "creator_url": "https://pixinvent.com/",             # URL website pembuat

    # Informasi template/aplikasi
    "template_name": "SERPTECH",                         # Nama aplikasi (muncul di sidebar & title)
    "template_suffix": "Django Admin Dashboard",         # Sub-judul aplikasi
    "template_version": "2.0.0",                         # Versi saat ini
    "template_free": False,                              # Apakah versi gratis? (False = berbayar/premium)

    # Deskripsi aplikasi — digunakan untuk SEO meta tag
    "template_description": "SERPTECH bukan sekadar aplikasi kasir biasa, melainkan Sistem Cloud ERP Terintegrasi (Enterprise Resource Planning) yang dirancang khusus untuk skala bisnis UMKM hingga Menengah di Indonesia.",

    # Keyword SEO — membantu search engine menemukan aplikasi
    "template_keyword": "django, django admin, dashboard, bootstrap 5 dashboard, bootstrap 5 design, bootstrap 5",

    # Link media sosial — ditampilkan di footer/about page
    "facebook_url": "https://www.facebook.com/pixinvents/",
    "twitter_url": "https://twitter.com/pixinvents",
    "github_url": "https://github.com/pixinvent",
    "dribbble_url": "https://dribbble.com/pixinvent",
    "instagram_url": "https://www.instagram.com/pixinvents/",

    # Link referensi — untuk halaman bantuan dan dokumentasi
    "license_url": "https://themeforest.net/licenses/standard",          # Halaman lisensi
    "live_preview": "https://demos.pixinvent.com/materialize-html-django-admin-template/demo-1/",  # Demo live
    "product_page": "https://1.envato.market/materialize_admin",          # Halaman produk
    "support": "https://pixinvent.ticksy.com/",                           # Halaman support/bantuan
    "more_themes": "https://1.envato.market/pixinvent_portfolio",         # Portfolio tema lainnya
    "documentation": "https://demos.pixinvent.com/materialize-html-admin-template/documentation",  # Dokumentasi
    "changelog": "https://demos.pixinvent.com/vuexy/changelog.html",      # Catatan perubahan versi
    "git_repository": "materialize-html-django-admin-template",           # Nama repo Git
    "git_repo_access": "https://tools.pixinvent.com/github/github-access",  # Akses repo Git
}


# ╔══════════════════════════════════════════════════════════════╗
# ║           DIREKTORI LAYOUT (THEME_LAYOUT_DIR)               ║
# ╚══════════════════════════════════════════════════════════════╝
#
# Direktori tempat file-file layout template berada.
# Path relatif dari folder 'templates/'.
# Contoh: "layout" → templates/layout/
#
# ⚠ JANGAN diubah kecuali Anda memindahkan folder layout
# ke lokasi lain di dalam templates/.
#
THEME_LAYOUT_DIR = "layout"
