"""
Views Pengaturan - Profil, Perusahaan, Template Cetak, Manajemen Data.
"""
import os
import shutil
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import transaction
from django.conf import settings
from web_project import TemplateLayout
from .models import PengaturanPerusahaan, TemplateCetak, BackupHistory

from .forms import PengaturanPerusahaanForm

class ProfilView(LoginRequiredMixin, TemplateView):
    template_name = 'pengaturan/profil.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        # Add profile to context so avatar and phone display correctly
        try:
            context['profile'] = self.request.user.profile
        except Exception:
            context['profile'] = None
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        new_password = request.POST.get('new_password', '')
        if new_password:
            user.set_password(new_password)
        user.save()
        
        # Update Profile
        try:
            profile = user.profile
            profile.phone = request.POST.get('phone', '')
            if request.POST.get('remove_avatar') == '1':
                profile.avatar = None
            elif request.FILES.get('avatar'):
                profile.avatar = request.FILES['avatar']
            profile.save()
        except Exception:
            pass

        messages.success(request, 'Profil berhasil diperbarui!')
        return redirect('pengaturan:profil')


class PerusahaanView(LoginRequiredMixin, UpdateView):
    model = PengaturanPerusahaan
    form_class = PengaturanPerusahaanForm
    template_name = 'pengaturan/perusahaan.html'
    success_url = reverse_lazy('pengaturan:perusahaan')

    def get_object(self, queryset=None):
        return PengaturanPerusahaan.load()

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Pengaturan perusahaan berhasil disimpan!')
        return super().form_valid(form)


class TemplateCetakListView(LoginRequiredMixin, ListView):
    model = TemplateCetak
    template_name = 'pengaturan/template_cetak_list.html'
    context_object_name = 'templates'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        for jenis, _ in TemplateCetak.JENIS_CHOICES:
            TemplateCetak.get_template(jenis)
        context['templates'] = TemplateCetak.objects.all()
        return context


class TemplateCetakCreateView(LoginRequiredMixin, CreateView):
    model = TemplateCetak
    template_name = 'pengaturan/template_cetak_form.html'
    fields = ['jenis', 'nama', 'header_nama_perusahaan', 'header_alamat', 'header_telepon', 'header_email', 'header_website', 'footer_ucapan', 'footer_keterangan', 'footer_copyright', 'signature_kiri_label', 'signature_kanan_label', 'tampilkan_logo', 'tampilkan_website', 'aktif']
    success_url = reverse_lazy('pengaturan:template_cetak_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['is_edit'] = False
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Template cetak berhasil dibuat!')
        return super().form_valid(form)


class TemplateCetakUpdateView(LoginRequiredMixin, UpdateView):
    model = TemplateCetak
    template_name = 'pengaturan/template_cetak_form.html'
    fields = ['jenis', 'nama', 'header_nama_perusahaan', 'header_alamat', 'header_telepon', 'header_email', 'header_website', 'footer_ucapan', 'footer_keterangan', 'footer_copyright', 'signature_kiri_label', 'signature_kanan_label', 'tampilkan_logo', 'tampilkan_website', 'aktif']
    success_url = reverse_lazy('pengaturan:template_cetak_list')

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Template cetak berhasil diperbarui!')
        return super().form_valid(form)


class ManajemenDataView(LoginRequiredMixin, TemplateView):
    template_name = 'pengaturan/manajemen_data.html'

    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        db_path = settings.DATABASES['default']['NAME']
        if os.path.exists(db_path):
            context['db_size'] = os.path.getsize(db_path)
            context['db_size_mb'] = round(os.path.getsize(db_path) / (1024 * 1024), 2)
        else:
            context['db_size'] = 0
            context['db_size_mb'] = 0
        from apps.licenses.models import Product, Client, LicenseKey
        from apps.pembelian.models import PembelianLisensi, PembelianLisensiItem
        from apps.automation.models import LogNotifikasi
        from .models import BackupHistory

        total_produk = Product.objects.count()
        total_klien = Client.objects.count()
        total_lisensi = LicenseKey.objects.count()
        total_transaksi = PembelianLisensi.objects.count()
        total_item = PembelianLisensiItem.objects.count()
        total_log_notifikasi = LogNotifikasi.objects.count()

        context['total_produk'] = total_produk
        context['total_klien'] = total_klien
        context['total_lisensi'] = total_lisensi
        context['total_master'] = total_produk + total_klien + total_lisensi
        context['total_transaksi'] = total_transaksi
        context['last_backup'] = BackupHistory.objects.filter(aksi='backup').order_by('-dibuat_pada').first()
        context['riwayat_list'] = BackupHistory.objects.all().order_by('-dibuat_pada')[:20]

        context['stats'] = {
            'produk': total_produk,
            'klien': total_klien,
            'lisensi': total_lisensi,
            'pembelian': total_transaksi,
            'item_pembelian': total_item,
            'log_notifikasi': total_log_notifikasi,
            'activity_log': 0, # Placeholder if activity log is not implemented
            'user': 1 # Placeholder, could count auth User
        }
        return context


@login_required
def backup_data(request):
    if request.method == 'POST':
        import datetime
        db_path = settings.DATABASES['default']['NAME']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"cls_backup_{timestamp}.sqlite3"
        backup_path = os.path.join(backup_dir, backup_filename)
        try:
            shutil.copy2(str(db_path), backup_path)
            file_size = os.path.getsize(backup_path)
            BackupHistory.objects.create(
                aksi='backup', nama_file=backup_filename,
                ukuran_file=file_size, user=request.user,
                catatan=f"Backup database oleh {request.user.username}"
            )
            response = HttpResponse(open(backup_path, 'rb').read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
            return response
        except Exception as e:
            messages.error(request, f'Gagal membuat backup: {str(e)}')
    return redirect('pengaturan:manajemen_data')


@login_required
def restore_data(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        import datetime
        db_path = settings.DATABASES['default']['NAME']
        backup_file = request.FILES['backup_file']
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        pre_restore = f"pre_restore_{timestamp}.sqlite3"
        try:
            shutil.copy2(str(db_path), os.path.join(backup_dir, pre_restore))
            with open(str(db_path), 'wb') as f:
                for chunk in backup_file.chunks():
                    f.write(chunk)
            BackupHistory.objects.create(
                aksi='restore', nama_file=backup_file.name,
                ukuran_file=backup_file.size, user=request.user,
                catatan=f"Restore oleh {request.user.username}. Pre-restore: {pre_restore}"
            )
            messages.success(request, 'Database berhasil di-restore! Silakan restart server.')
        except Exception as e:
            messages.error(request, f'Gagal restore: {str(e)}')
    return redirect('pengaturan:manajemen_data')


@login_required
def reset_data(request):
    if request.method == 'POST':
        konfirmasi = request.POST.get('konfirmasi', '')
        if konfirmasi == 'HAPUS SEMUA':
            try:
                from apps.licenses.models import Product, Client, LicenseKey
                from apps.pembelian.models import PembelianLisensi, PembelianLisensiItem
                with transaction.atomic():
                    PembelianLisensiItem.objects.all().delete()
                    PembelianLisensi.objects.all().delete()
                    LicenseKey.objects.all().delete()
                    Client.objects.all().delete()
                    Product.objects.all().delete()
                    BackupHistory.objects.create(
                        aksi='reset', user=request.user,
                        catatan=f"Reset data oleh {request.user.username}"
                    )
                messages.success(request, 'Semua data berhasil direset!')
            except Exception as e:
                messages.error(request, f'Gagal reset: {str(e)}')
        else:
            messages.warning(request, 'Konfirmasi tidak valid. Ketik HAPUS SEMUA untuk mengonfirmasi.')
    return redirect('pengaturan:manajemen_data')


@login_required
def api_database_stats(request):
    from apps.licenses.models import Product, Client, LicenseKey
    db_path = settings.DATABASES['default']['NAME']
    return JsonResponse({
        'db_size_mb': round(os.path.getsize(db_path) / (1024 * 1024), 2) if os.path.exists(db_path) else 0,
        'total_produk': Product.objects.count(),
        'total_klien': Client.objects.count(),
        'total_lisensi': LicenseKey.objects.count(),
    })
