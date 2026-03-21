from django.urls import path
from . import views

app_name = 'laporan'

urlpatterns = [
    path('lisensi/', views.LaporanLisensiView.as_view(), name='lisensi'),
    path('klien/', views.LaporanKlienView.as_view(), name='klien'),
    path('pendapatan/', views.LaporanPendapatanView.as_view(), name='pendapatan'),
    path('keuangan/', views.LaporanKeuanganView.as_view(), name='keuangan'),
]
