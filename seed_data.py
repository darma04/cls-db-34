"""
Script untuk membuat data testing SIMKOS.
Jalankan: python manage.py shell < seed_data.py
"""
import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from apps.properti.models import Properti, TipeKamar, Kamar
from apps.penyewa.models import Penyewa
from apps.sewa.models import KontrakSewa, TagihanSewa, PembayaranSewa
from datetime import date, datetime
from decimal import Decimal

print("=== Membuat Data Testing SIMKOS ===\n")

# Get or create user
user = User.objects.first()
if not user:
    user = User.objects.create_superuser('admin', 'admin@simkos.com', 'admin123')
    print("✓ User admin dibuat")

# ══════════════════════════════════════
# TIPE KAMAR
# ══════════════════════════════════════
tipe_data = [
    {'nama': 'Standard', 'harga_bulanan': 800000, 'fasilitas': 'Kasur, Lemari, Meja, Kursi', 'deskripsi': 'Kamar standar dengan fasilitas dasar'},
    {'nama': 'AC', 'harga_bulanan': 1200000, 'fasilitas': 'AC, Kasur, Lemari, Meja, Kursi, WiFi', 'deskripsi': 'Kamar dengan AC dan WiFi'},
    {'nama': 'VIP', 'harga_bulanan': 2000000, 'fasilitas': 'AC, Kasur Spring Bed, Lemari, Meja, Kursi, WiFi, Kamar Mandi Dalam, TV', 'deskripsi': 'Kamar VIP fasilitas lengkap'},
]
tipe_list = []
for t in tipe_data:
    obj, created = TipeKamar.objects.get_or_create(nama=t['nama'], defaults=t)
    tipe_list.append(obj)
    if created:
        print(f"  ✓ Tipe Kamar: {obj.nama}")
print(f"✓ {len(tipe_list)} Tipe Kamar siap\n")

# ══════════════════════════════════════
# PROPERTI
# ══════════════════════════════════════
prop_data = [
    {
        'nama': 'Kost Melati Indah',
        'tipe': 'kost',
        'alamat': 'Jl. Melati No. 45, RT 03/RW 07, Kel. Sukamaju',
        'kota': 'Bandung',
        'deskripsi': 'Kost nyaman dan strategis dekat kampus ITB',
        'pemilik': 'Budi Santoso',
        'telepon': '08123456789',
        'aktif': True,
        'dibuat_oleh': user,
    },
    {
        'nama': 'Kontrakan Dahlia Asri',
        'tipe': 'kontrakan',
        'alamat': 'Jl. Dahlia Raya No. 12, Kel. Cimahi Tengah',
        'kota': 'Cimahi',
        'deskripsi': 'Kontrakan luas cocok untuk keluarga',
        'pemilik': 'Siti Rahmawati',
        'telepon': '08198765432',
        'aktif': True,
        'dibuat_oleh': user,
    },
]
prop_list = []
for p in prop_data:
    obj, created = Properti.objects.get_or_create(nama=p['nama'], defaults=p)
    prop_list.append(obj)
    if created:
        print(f"  ✓ Properti: {obj.nama}")
print(f"✓ {len(prop_list)} Properti siap\n")

# ══════════════════════════════════════
# KAMAR - Kost Melati (2 lantai, 8 kamar)
# ══════════════════════════════════════
kamar_melati = [
    # Lantai 1
    {'nomor_kamar': '101', 'lantai': 1, 'tipe_kamar': tipe_list[0], 'status': 'terisi', 'pos_x': 20, 'pos_y': 20, 'width': 120, 'height': 100},
    {'nomor_kamar': '102', 'lantai': 1, 'tipe_kamar': tipe_list[1], 'status': 'terisi', 'pos_x': 160, 'pos_y': 20, 'width': 120, 'height': 100},
    {'nomor_kamar': '103', 'lantai': 1, 'tipe_kamar': tipe_list[0], 'status': 'tersedia', 'pos_x': 300, 'pos_y': 20, 'width': 120, 'height': 100},
    {'nomor_kamar': '104', 'lantai': 1, 'tipe_kamar': tipe_list[2], 'status': 'maintenance', 'pos_x': 440, 'pos_y': 20, 'width': 140, 'height': 100},
    # Lantai 2
    {'nomor_kamar': '201', 'lantai': 2, 'tipe_kamar': tipe_list[1], 'status': 'terisi', 'pos_x': 20, 'pos_y': 20, 'width': 120, 'height': 100},
    {'nomor_kamar': '202', 'lantai': 2, 'tipe_kamar': tipe_list[1], 'status': 'tersedia', 'pos_x': 160, 'pos_y': 20, 'width': 120, 'height': 100},
    {'nomor_kamar': '203', 'lantai': 2, 'tipe_kamar': tipe_list[2], 'status': 'terisi', 'pos_x': 300, 'pos_y': 20, 'width': 140, 'height': 100},
    {'nomor_kamar': '204', 'lantai': 2, 'tipe_kamar': tipe_list[0], 'status': 'tersedia', 'pos_x': 460, 'pos_y': 20, 'width': 120, 'height': 100},
]
kamar_list_all = []
for k in kamar_melati:
    obj, created = Kamar.objects.get_or_create(
        properti=prop_list[0], nomor_kamar=k['nomor_kamar'],
        defaults={**k, 'properti': prop_list[0]}
    )
    kamar_list_all.append(obj)
    if created:
        print(f"  ✓ Kamar: Melati - {obj.nomor_kamar} (Lt.{obj.lantai})")

# Kontrakan Dahlia (3 unit)
kamar_dahlia = [
    {'nomor_kamar': 'A1', 'lantai': 1, 'tipe_kamar': tipe_list[2], 'status': 'terisi', 'pos_x': 20, 'pos_y': 20, 'width': 160, 'height': 120},
    {'nomor_kamar': 'A2', 'lantai': 1, 'tipe_kamar': tipe_list[2], 'status': 'tersedia', 'pos_x': 200, 'pos_y': 20, 'width': 160, 'height': 120},
    {'nomor_kamar': 'A3', 'lantai': 1, 'tipe_kamar': tipe_list[1], 'status': 'terisi', 'pos_x': 380, 'pos_y': 20, 'width': 160, 'height': 120},
]
for k in kamar_dahlia:
    obj, created = Kamar.objects.get_or_create(
        properti=prop_list[1], nomor_kamar=k['nomor_kamar'],
        defaults={**k, 'properti': prop_list[1]}
    )
    kamar_list_all.append(obj)
    if created:
        print(f"  ✓ Kamar: Dahlia - {obj.nomor_kamar}")
print(f"✓ {len(kamar_list_all)} Kamar siap\n")

# ══════════════════════════════════════
# PENYEWA
# ══════════════════════════════════════
penyewa_data = [
    {'nama': 'Ahmad Fauzi', 'nik': '3201011234560001', 'jenis_kelamin': 'L', 'telepon': '081234567890', 'email': 'ahmad@email.com', 'alamat_asal': 'Jl. Merdeka No. 10, Jakarta Selatan', 'pekerjaan': 'Mahasiswa ITB', 'status': 'aktif', 'dibuat_oleh': user},
    {'nama': 'Sari Dewi Lestari', 'nik': '3201011234560002', 'jenis_kelamin': 'P', 'telepon': '081234567891', 'email': 'sari@email.com', 'alamat_asal': 'Jl. Sudirman No. 25, Surabaya', 'pekerjaan': 'Karyawan Swasta', 'status': 'aktif', 'dibuat_oleh': user},
    {'nama': 'Rizky Pratama', 'nik': '3201011234560003', 'jenis_kelamin': 'L', 'telepon': '081234567892', 'email': 'rizky@email.com', 'alamat_asal': 'Jl. Pahlawan No. 5, Medan', 'pekerjaan': 'Mahasiswa UNPAD', 'status': 'aktif', 'dibuat_oleh': user},
    {'nama': 'Nurul Hidayah', 'nik': '3201011234560004', 'jenis_kelamin': 'P', 'telepon': '081234567893', 'email': 'nurul@email.com', 'alamat_asal': 'Jl. Diponegoro No. 30, Yogyakarta', 'pekerjaan': 'Freelancer', 'status': 'aktif', 'dibuat_oleh': user},
    {'nama': 'Dedi Kurniawan', 'nik': '3201011234560005', 'jenis_kelamin': 'L', 'telepon': '081234567894', 'email': 'dedi@email.com', 'alamat_asal': 'Jl. Ahmad Yani No. 15, Semarang', 'pekerjaan': 'Pedagang', 'status': 'aktif', 'dibuat_oleh': user},
]
penyewa_list = []
for p in penyewa_data:
    obj, created = Penyewa.objects.get_or_create(nik=p['nik'], defaults=p)
    penyewa_list.append(obj)
    if created:
        print(f"  ✓ Penyewa: {obj.nama}")
print(f"✓ {len(penyewa_list)} Penyewa siap\n")

# ══════════════════════════════════════
# KONTRAK SEWA (5 kontrak aktif)
# ══════════════════════════════════════
# Kamar terisi: Melati 101(idx0), 102(idx1), 201(idx4), 203(idx6), Dahlia A1(idx8), A3(idx10)
kontrak_data = [
    {'penyewa': penyewa_list[0], 'kamar': kamar_list_all[0], 'tanggal_masuk': date(2025, 10, 1), 'tanggal_keluar': date(2026, 9, 30), 'harga_sewa': 800000, 'deposit': 800000},
    {'penyewa': penyewa_list[1], 'kamar': kamar_list_all[1], 'tanggal_masuk': date(2025, 11, 1), 'tanggal_keluar': date(2026, 10, 31), 'harga_sewa': 1200000, 'deposit': 1200000},
    {'penyewa': penyewa_list[2], 'kamar': kamar_list_all[4], 'tanggal_masuk': date(2025, 12, 1), 'tanggal_keluar': date(2026, 11, 30), 'harga_sewa': 1200000, 'deposit': 1200000},
    {'penyewa': penyewa_list[3], 'kamar': kamar_list_all[6], 'tanggal_masuk': date(2026, 1, 1), 'tanggal_keluar': date(2026, 12, 31), 'harga_sewa': 2000000, 'deposit': 2000000},
    {'penyewa': penyewa_list[4], 'kamar': kamar_list_all[8], 'tanggal_masuk': date(2026, 1, 15), 'tanggal_keluar': date(2027, 1, 14), 'harga_sewa': 2000000, 'deposit': 2000000},
]
kontrak_list = []
for kd in kontrak_data:
    existing = KontrakSewa.objects.filter(penyewa=kd['penyewa'], kamar=kd['kamar'], status='aktif').first()
    if existing:
        kontrak_list.append(existing)
    else:
        obj = KontrakSewa(
            penyewa=kd['penyewa'], kamar=kd['kamar'],
            tanggal_masuk=kd['tanggal_masuk'], tanggal_keluar=kd['tanggal_keluar'],
            harga_sewa=kd['harga_sewa'], deposit=kd['deposit'],
            status='aktif', dibuat_oleh=user
        )
        obj.save()
        kontrak_list.append(obj)
        print(f"  ✓ Kontrak: {obj.nomor_kontrak} - {obj.penyewa.nama}")
print(f"✓ {len(kontrak_list)} Kontrak siap\n")

# ══════════════════════════════════════
# TAGIHAN SEWA (Februari 2026)
# ══════════════════════════════════════
tagihan_list = []
for kontrak in kontrak_list:
    existing = TagihanSewa.objects.filter(kontrak=kontrak, periode_bulan=2, periode_tahun=2026).first()
    if existing:
        tagihan_list.append(existing)
    else:
        tagihan = TagihanSewa(
            kontrak=kontrak,
            periode_bulan=2,
            periode_tahun=2026,
            jumlah=kontrak.harga_sewa,
            tanggal_jatuh_tempo=date(2026, 2, 10),
            status='belum_bayar',
            dibuat_oleh=user
        )
        tagihan.save()
        tagihan_list.append(tagihan)
        print(f"  ✓ Tagihan: {tagihan.nomor_tagihan} - Rp {tagihan.jumlah:,.0f}")

# Buat juga tagihan Januari 2026 (sudah lunas) + pembayaran
for kontrak in kontrak_list[:3]:
    existing = TagihanSewa.objects.filter(kontrak=kontrak, periode_bulan=1, periode_tahun=2026).first()
    if not existing:
        tagihan_jan = TagihanSewa(
            kontrak=kontrak, periode_bulan=1, periode_tahun=2026,
            jumlah=kontrak.harga_sewa, tanggal_jatuh_tempo=date(2026, 1, 10),
            status='lunas', dibuat_oleh=user
        )
        tagihan_jan.save()
        # Buat pembayaran
        bayar = PembayaranSewa(
            tagihan=tagihan_jan, tanggal_bayar=date(2026, 1, 8),
            jumlah_bayar=kontrak.harga_sewa, metode_bayar='transfer',
            dicatat_oleh=user
        )
        bayar.save()
        print(f"  ✓ Tagihan Jan + Bayar: {tagihan_jan.nomor_tagihan}")

# Bayar 2 tagihan Feb sebagian
if tagihan_list and len(tagihan_list) >= 2:
    # Bayar tagihan pertama lunas
    t0 = tagihan_list[0]
    if not PembayaranSewa.objects.filter(tagihan=t0).exists():
        bayar = PembayaranSewa(
            tagihan=t0, tanggal_bayar=date(2026, 2, 5),
            jumlah_bayar=t0.jumlah, metode_bayar='transfer', dicatat_oleh=user
        )
        bayar.save()
        print(f"  ✓ Pembayaran lunas: {t0.nomor_tagihan}")

    # Bayar tagihan kedua sebagian
    t1 = tagihan_list[1]
    if not PembayaranSewa.objects.filter(tagihan=t1).exists():
        bayar = PembayaranSewa(
            tagihan=t1, tanggal_bayar=date(2026, 2, 8),
            jumlah_bayar=Decimal('500000'), metode_bayar='tunai', dicatat_oleh=user
        )
        bayar.save()
        print(f"  ✓ Pembayaran sebagian: {t1.nomor_tagihan}")

print(f"\n✓ Tagihan dan Pembayaran siap")
print("\n=== SEED DATA SELESAI ===")
print(f"  Properti: {Properti.objects.count()}")
print(f"  Tipe Kamar: {TipeKamar.objects.count()}")
print(f"  Kamar: {Kamar.objects.count()}")
print(f"  Penyewa: {Penyewa.objects.count()}")
print(f"  Kontrak: {KontrakSewa.objects.count()}")
print(f"  Tagihan: {TagihanSewa.objects.count()}")
print(f"  Pembayaran: {PembayaranSewa.objects.count()}")
