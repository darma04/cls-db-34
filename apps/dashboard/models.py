"""
==========================================================================
 DASHBOARD MODELS - Tidak Ada Model (Aggregation Module)
==========================================================================
 Dashboard tidak memerlukan models sendiri karena semua data
 di-aggregate dari models modul lain:
 - Produk, Stok, Gudang (modul produk)
 - SalesOrder, POSTransaction (modul penjualan & pos)
 - PurchaseOrder (modul pembelian)
 - TransaksiBiaya (modul biaya)
 - UserActivity (modul activity_log)

 Semua kalkulasi dilakukan langsung di DashboardView (views.py).
==========================================================================
"""
# Tidak ada models — dashboard hanya menampilkan aggregasi data
