from django.urls import path
from . import views_ui

app_name = 'licenses_ui'

urlpatterns = [
    # Client CRUD
    path('clients/', views_ui.ClientListView.as_view(), name='client_list'),
    path('clients/create/', views_ui.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/update/', views_ui.ClientUpdateView.as_view(), name='client_update'),
    path('clients/<int:pk>/delete/', views_ui.ClientDeleteView.as_view(), name='client_delete'),

    # Product CRUD
    path('products/', views_ui.ProductListView.as_view(), name='product_list'),
    path('products/create/', views_ui.ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/update/', views_ui.ProductUpdateView.as_view(), name='product_update'),
    path('products/<int:pk>/delete/', views_ui.ProductDeleteView.as_view(), name='product_delete'),

    # LicenseKey CRUD + Detail
    path('keys/', views_ui.LicenseKeyListView.as_view(), name='licensekey_list'),
    path('keys/create/', views_ui.LicenseKeyCreateView.as_view(), name='licensekey_create'),
    path('keys/<int:pk>/', views_ui.LicenseKeyDetailView.as_view(), name='licensekey_detail'),
    path('keys/<int:pk>/update/', views_ui.LicenseKeyUpdateView.as_view(), name='licensekey_update'),
    path('keys/<int:pk>/delete/', views_ui.LicenseKeyDeleteView.as_view(), name='licensekey_delete'),

    # AJAX: Unlink Device
    path('device/<int:pk>/unlink/', views_ui.unlink_device, name='unlink_device'),
]

