from django.urls import path
from . import views

app_name = 'pengaturan'

urlpatterns = [
    path('profil/', views.ProfilView.as_view(), name='profil'),
    path('perusahaan/', views.PerusahaanView.as_view(), name='perusahaan'),
    path('template-cetak/', views.TemplateCetakListView.as_view(), name='template_cetak_list'),
    path('template-cetak/tambah/', views.TemplateCetakCreateView.as_view(), name='template_cetak_create'),
    path('template-cetak/<int:pk>/edit/', views.TemplateCetakUpdateView.as_view(), name='template_cetak_update'),
    path('manajemen-data/', views.ManajemenDataView.as_view(), name='manajemen_data'),
    path('manajemen-data/backup/', views.backup_data, name='backup_data'),
    path('manajemen-data/restore/', views.restore_data, name='restore_data'),
    path('manajemen-data/reset/', views.reset_data, name='reset_data'),
    path('api/database-stats/', views.api_database_stats, name='api_database_stats'),
]
