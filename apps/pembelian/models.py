"""
Model Pembelian Lisensi untuk Central License Server.
PembelianLisensi (transaksi pembelian) dan PembelianLisensiItem (detail item).
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class PembelianLisensi(models.Model):
    """Record transaksi pembelian lisensi oleh klien."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Dikonfirmasi'),
        ('completed', 'Selesai'),
        ('cancelled', 'Dibatalkan'),
    ]

    nomor_transaksi = models.CharField(max_length=50, unique=True, verbose_name="Nomor Transaksi")
    klien = models.ForeignKey('licenses.Client', on_delete=models.CASCADE, verbose_name="Klien")
    tanggal = models.DateField(default=timezone.now, verbose_name="Tanggal Pembelian")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    catatan = models.TextField(blank=True, verbose_name="Catatan")
    total_harga = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Total Harga")

    dibuat_oleh = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Dibuat Oleh")
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diupdate_pada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pembelian Lisensi"
        verbose_name_plural = "Pembelian Lisensi"
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f"{self.nomor_transaksi} - {self.klien.name}"

    def save(self, *args, **kwargs):
        if not self.nomor_transaksi:
            today = timezone.now()
            prefix = f"TRX-{today.strftime('%Y%m')}"
            last = PembelianLisensi.objects.filter(
                nomor_transaksi__startswith=prefix
            ).order_by('-nomor_transaksi').first()
            if last:
                try:
                    last_num = int(last.nomor_transaksi.split('-')[-1])
                    next_num = last_num + 1
                except (ValueError, IndexError):
                    next_num = 1
            else:
                next_num = 1
            self.nomor_transaksi = f"{prefix}-{next_num:04d}"
        super().save(*args, **kwargs)

    def update_total(self):
        total = self.items.aggregate(total=models.Sum('subtotal'))['total'] or 0
        self.total_harga = total
        self.save(update_fields=['total_harga'])


class PembelianLisensiItem(models.Model):
    """Detail item per pembelian lisensi."""
    pembelian = models.ForeignKey(PembelianLisensi, on_delete=models.CASCADE, related_name='items', verbose_name="Pembelian")
    produk = models.ForeignKey('licenses.Product', on_delete=models.CASCADE, verbose_name="Produk")
    jumlah = models.PositiveIntegerField(default=1, verbose_name="Jumlah Lisensi")
    durasi_hari = models.PositiveIntegerField(default=365, verbose_name="Durasi (Hari)")
    harga_satuan = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Harga Satuan")
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name="Subtotal")

    class Meta:
        verbose_name = "Item Pembelian"
        verbose_name_plural = "Item Pembelian"

    def __str__(self):
        return f"{self.produk.name} x{self.jumlah}"

    def save(self, *args, **kwargs):
        self.subtotal = self.harga_satuan * self.jumlah
        super().save(*args, **kwargs)
