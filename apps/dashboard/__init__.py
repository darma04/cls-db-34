"""
==========================================================================
 DASHBOARD APP - Halaman Utama Dashboard ERP
==========================================================================
 Package ini menampilkan halaman dashboard dengan statistik dan grafik
 dari SEMUA modul bisnis.

 Berisi:
 - views.py → DashboardView — mengagregasi data dari semua modul
 - urls.py  → Routing URL dashboard

 Data yang ditampilkan di dashboard:
 - Total produk, kategori, stok rendah (dari apps/produk)
 - Total penjualan, customer aktif (dari apps/penjualan & apps/pos)
 - Total pembelian, supplier (dari apps/pembelian)
 - Total biaya operasional (dari apps/biaya)
 - Total karyawan, absensi (dari apps/hr)
 - Grafik penjualan harian/bulanan
 - Top produk terlaris
 - Aktivitas terbaru (dari apps/activity_log)

 Terhubung dengan SEMUA modul bisnis lainnya (read-only).
==========================================================================
"""
