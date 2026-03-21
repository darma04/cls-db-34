"""
==========================================================================
 LICENSES ADMIN — Konfigurasi Django Admin Panel
==========================================================================
"""
from django.contrib import admin
from .models import Product, Client, LicenseKey, DeviceBinding, LicenseLog


class DeviceBindingInline(admin.TabularInline):
    """Inline untuk melihat perangkat terikat di halaman LicenseKey Admin."""
    model = DeviceBinding
    extra = 0
    readonly_fields = ('hardware_id', 'device_name', 'ip_address', 'domain', 'first_seen', 'last_seen')
    can_delete = True


class LicenseLogInline(admin.TabularInline):
    """Inline untuk melihat log aktivitas di halaman LicenseKey Admin."""
    model = LicenseLog
    extra = 0
    readonly_fields = ('action', 'detail', 'ip_address', 'hardware_id', 'timestamp')
    can_delete = False
    max_num = 0  # Tidak bisa menambah log via admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')


@admin.register(LicenseKey)
class LicenseKeyAdmin(admin.ModelAdmin):
    list_display = ('key', 'product', 'client', 'is_activated', 'status', 'max_devices', 'expires_at')
    list_filter = ('status', 'is_activated', 'product')
    search_fields = ('key', 'client__name', 'registered_domain')
    readonly_fields = ('key', 'activated_at', 'expires_at', 'created_at', 'updated_at')
    inlines = [DeviceBindingInline, LicenseLogInline]


@admin.register(DeviceBinding)
class DeviceBindingAdmin(admin.ModelAdmin):
    list_display = ('license', 'hardware_id', 'device_name', 'ip_address', 'is_active', 'last_seen')
    list_filter = ('is_active',)
    search_fields = ('hardware_id', 'device_name', 'license__key')
    readonly_fields = ('first_seen', 'last_seen')


@admin.register(LicenseLog)
class LicenseLogAdmin(admin.ModelAdmin):
    list_display = ('license', 'action', 'ip_address', 'hardware_id', 'timestamp')
    list_filter = ('action',)
    search_fields = ('license__key', 'detail', 'ip_address')
    readonly_fields = ('license', 'action', 'detail', 'ip_address', 'hardware_id', 'timestamp')
