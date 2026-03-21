from django.urls import path
from . import views

app_name = 'pembelian'

urlpatterns = [
    path('', views.PembelianListView.as_view(), name='pembelian_list'),
    path('tambah/', views.PembelianCreateView.as_view(), name='pembelian_create'),
    path('<int:pk>/', views.PembelianDetailView.as_view(), name='pembelian_detail'),
    path('<int:pk>/status/', views.pembelian_update_status, name='pembelian_update_status'),
    path('<int:pk>/hapus/', views.pembelian_delete, name='pembelian_delete'),
]
