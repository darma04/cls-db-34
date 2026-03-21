"""
AI Assistant Intents - Deteksi intent dan pengumpulan data
untuk Central License Server (Manajemen Lisensi).
"""
import logging
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum, Count, Q

logger = logging.getLogger(__name__)

INTENT_KEYWORDS = {
    'lisensi': [
        'lisensi', 'license', 'kunci', 'key', 'aktivasi', 'aktif',
        'kadaluarsa', 'expired', 'suspend', 'ditangguhkan', 'domain',
    ],
    'produk': [
        'produk', 'product', 'software', 'aplikasi', 'app', 'kode produk',
    ],
    'klien': [
        'klien', 'client', 'pelanggan', 'customer', 'pembeli',
        'data klien', 'email klien', 'telepon klien',
    ],
    'pendapatan': [
        'pendapatan', 'income', 'pemasukan', 'revenue', 'omzet',
        'penjualan', 'pembelian', 'transaksi', 'uang',
    ],
    'keuangan': [
        'keuangan', 'finance', 'laba', 'rugi', 'profit', 'keuntungan',
        'laporan keuangan', 'rekap',
    ],
    'bantuan': [
        'bantuan', 'help', 'tolong', 'cara', 'panduan', 'tutorial',
        'fitur', 'menu', 'apa saja', 'bisa apa',
    ],
    'executive_summary': [
        'executive summary', 'ringkasan', 'summary', 'overview', 'ikhtisar',
    ],
    'forecasting': [
        'prediksi', 'forecast', 'proyeksi', 'estimasi', 'perkiraan', 'tren',
    ],
}


def detect_intent(message):
    msg = message.lower().strip()
    best_intent = 'umum'
    best_score = 0
    for intent, keywords in INTENT_KEYWORDS.items():
        score = sum(len(kw) for kw in keywords if kw in msg)
        if score > best_score:
            best_score = score
            best_intent = intent
    return best_intent


def gather_data(intent, message=''):
    today = timezone.now().date()
    try:
        if intent == 'lisensi':
            return _gather_lisensi(today)
        elif intent == 'produk':
            return _gather_produk()
        elif intent == 'klien':
            return _gather_klien()
        elif intent == 'pendapatan':
            return _gather_pendapatan(today)
        elif intent == 'keuangan':
            return _gather_keuangan(today)
        elif intent == 'bantuan':
            return _gather_bantuan()
        elif intent == 'executive_summary':
            return _gather_executive_summary(today)
        elif intent == 'forecasting':
            return _gather_forecasting(today)
        else:
            return _gather_umum(today)
    except Exception as e:
        logger.error(f"Error gathering data for intent '{intent}': {e}")
        return {'intent': intent, 'error': True, 'ringkasan': f'Error: {str(e)}'}


def _gather_lisensi(today):
    from apps.licenses.models import LicenseKey
    total = LicenseKey.objects.count()
    aktif = LicenseKey.objects.filter(status='active').count()
    kadaluarsa = LicenseKey.objects.filter(status='expired').count()
    suspended = LicenseKey.objects.filter(status='suspended').count()
    teraktivasi = LicenseKey.objects.filter(is_activated=True).count()
    segera = LicenseKey.objects.filter(
        status='active', expires_at__lte=timezone.now() + timedelta(days=30),
        expires_at__gte=timezone.now()
    ).count()
    ringkasan = f"""Data Lisensi Central License Server:
- Total Lisensi: {total}
- Aktif: {aktif}
- Kadaluarsa: {kadaluarsa}
- Ditangguhkan: {suspended}
- Sudah Teraktivasi: {teraktivasi}
- Segera Kadaluarsa (30 hari): {segera}"""
    return {'intent': 'lisensi', 'ringkasan': ringkasan}


def _gather_produk():
    from apps.licenses.models import Product
    products = Product.objects.annotate(
        total_lisensi=Count('licenses'),
        lisensi_aktif=Count('licenses', filter=Q(licenses__status='active'))
    ).order_by('name')
    product_list = [f"- {p.name} ({p.code}): {p.total_lisensi} lisensi ({p.lisensi_aktif} aktif)" for p in products]
    ringkasan = f"""Data Produk Software:
- Total Produk: {products.count()}

Detail Produk:
{chr(10).join(product_list) if product_list else '- Belum ada produk'}"""
    return {'intent': 'produk', 'ringkasan': ringkasan}


def _gather_klien():
    from apps.licenses.models import Client
    total = Client.objects.count()
    klien_list = Client.objects.annotate(
        total_lisensi=Count('licenses')
    ).order_by('-total_lisensi')[:10]
    kl = [f"- {k.name}: {k.total_lisensi} lisensi" for k in klien_list]
    ringkasan = f"""Data Klien:
- Total Klien: {total}

Top 10 Klien (berdasarkan jumlah lisensi):
{chr(10).join(kl) if kl else '- Belum ada klien'}"""
    return {'intent': 'klien', 'ringkasan': ringkasan}


def _gather_pendapatan(today):
    try:
        from apps.pembelian.models import PembelianLisensi
        total = float(PembelianLisensi.objects.filter(status='completed').aggregate(t=Sum('total_harga'))['t'] or 0)
        bulan_ini = today.replace(day=1)
        pendapatan_bulan = float(PembelianLisensi.objects.filter(
            status='completed', tanggal__gte=bulan_ini
        ).aggregate(t=Sum('total_harga'))['t'] or 0)
        trx_count = PembelianLisensi.objects.filter(status='completed').count()
    except Exception:
        total = pendapatan_bulan = trx_count = 0
    ringkasan = f"""Data Pendapatan:
- Total Pendapatan Keseluruhan: Rp {total:,.0f}
- Pendapatan Bulan Ini: Rp {pendapatan_bulan:,.0f}
- Total Transaksi Selesai: {trx_count}"""
    return {'intent': 'pendapatan', 'ringkasan': ringkasan}


def _gather_keuangan(today):
    lisensi = _gather_lisensi(today)
    pendapatan = _gather_pendapatan(today)
    ringkasan = f"""Laporan Keuangan Central License Server:

{lisensi['ringkasan']}

{pendapatan['ringkasan']}"""
    return {'intent': 'keuangan', 'ringkasan': ringkasan}


def _gather_bantuan():
    ringkasan = """Panduan Central License Server:

Modul yang tersedia:
1. Dashboard — Ringkasan data lisensi dan statistik
2. Data Produk — Kelola produk software
3. Data Klien — Kelola data pelanggan
4. Kunci Lisensi — Generate dan kelola kunci lisensi
5. Laporan — Laporan lisensi, klien, pendapatan, keuangan
6. AI Manajemen — Chat AI untuk analisa data
7. Log Aktivitas — Audit trail semua aktivitas
8. Telegram — Notifikasi otomatis via Telegram
9. Pengaturan — Konfigurasi sistem
10. Pembelian Lisensi — Kelola transaksi pembelian

Contoh pertanyaan:
- "Berapa lisensi aktif saat ini?"
- "Tampilkan data klien terbanyak"
- "Berapa pendapatan bulan ini?"
- "Lisensi mana yang segera kadaluarsa?"
"""
    return {'intent': 'bantuan', 'ringkasan': ringkasan}


def _gather_executive_summary(today):
    lisensi = _gather_lisensi(today)
    pendapatan = _gather_pendapatan(today)
    ringkasan = f"""INSTRUKSI: Buat EXECUTIVE SUMMARY ringkas untuk Central License Server.

{lisensi['ringkasan']}

{pendapatan['ringkasan']}"""
    return {'intent': 'executive_summary', 'ringkasan': ringkasan}


def _gather_forecasting(today):
    data = _gather_lisensi(today)
    ringkasan = f"""INSTRUKSI: Buat prediksi/forecast berdasarkan data berikut.

{data['ringkasan']}"""
    return {'intent': 'forecasting', 'ringkasan': ringkasan}


def _gather_umum(today):
    return _gather_lisensi(today)
