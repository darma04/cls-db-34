"""
==========================================================================
 DASHBOARD ADMIN - Dashboard tidak punya model sendiri
==========================================================================
 Dashboard mengumpulkan data dari modul lain (produk, pos, penjualan, dll.)
 sehingga tidak perlu registrasi model di Django Admin.
==========================================================================
"""
from django.contrib import admin
# Dashboard tidak punya model — hanya mengumpulkan data dari modul lain
