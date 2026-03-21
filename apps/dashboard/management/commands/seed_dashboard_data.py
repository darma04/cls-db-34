"""
==========================================================================
 SEED DASHBOARD DATA - Management Command Generate Data Contoh
==========================================================================
 Perintah CLI untuk membuat data contoh (seed data) ke database.
 Berguna untuk testing dan demo dashboard.

 Data yang dibuat:
 - Kategori produk (5), Satuan (5), Gudang (2)
 - Produk (25) dengan harga beli/jual dan stok per gudang
 - Customer (10) dengan data kontak
 - Sales Order (30) dengan items dan total terhitung

 Cara pakai:
   python manage.py seed_dashboard_data           # Generate data baru
   python manage.py seed_dashboard_data --clear   # Hapus data lama + generate baru

 PERINGATAN: Perintah --clear akan MENGHAPUS semua data terkait!
==========================================================================
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
import random
from datetime import timedelta


class Command(BaseCommand):
    """
    Management command untuk membuat data contoh (seed) dashboard ERP.
    Membuat kategori, satuan, gudang, produk, customer, dan sales order
    secara otomatis untuk keperluan testing dan demo.
    """
    help = 'Generate sample data untuk dashboard ERP'

    def add_arguments(self, parser):
        """Tambahkan argumen CLI --clear untuk menghapus data lama."""
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Hapus semua data sebelum generate data baru',
        )

    def handle(self, *args, **options):
        """
        Fungsi utama yang dijalankan saat command dipanggil.
        Membuat data contoh secara berurutan: Kategori → Satuan → Gudang → Produk → Customer → SO.
        """
        from apps.produk.models import Kategori, Satuan, Produk, Gudang, Stok
        from apps.penjualan.models import Customer, SalesOrder, SalesOrderItem

        if options['clear']:
            self.stdout.write(self.style.WARNING('Menghapus data lama...'))
            SalesOrderItem.objects.all().delete()
            SalesOrder.objects.all().delete()
            Customer.objects.all().delete()
            Stok.objects.all().delete()
            Produk.objects.all().delete()
            Gudang.objects.all().delete()
            Satuan.objects.all().delete()
            Kategori.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Data lama berhasil dihapus!'))

        # Ambil atau buat user admin sebagai pembuat data
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin/admin123'))

        # 1. Buat Kategori produk (5 kategori)
        self.stdout.write('Membuat Kategori...')
        kategori_data = [
            {'nama': 'Elektronik', 'deskripsi': 'Produk elektronik dan gadget'},
            {'nama': 'Fashion', 'deskripsi': 'Pakaian dan aksesoris'},
            {'nama': 'Makanan & Minuman', 'deskripsi': 'Produk makanan dan minuman'},
            {'nama': 'Peralatan Rumah', 'deskripsi': 'Peralatan rumah tangga'},
            {'nama': 'Olahraga', 'deskripsi': 'Peralatan olahraga'},
        ]
        
        kategori_list = []
        for data in kategori_data:
            kategori, created = Kategori.objects.get_or_create(
                nama=data['nama'],
                defaults={'deskripsi': data['deskripsi'], 'dibuat_oleh': admin_user}
            )
            kategori_list.append(kategori)
            if created:
                self.stdout.write(f'  ✓ {kategori.nama}')

        # 2. Buat Satuan ukuran (5 satuan)
        self.stdout.write('Membuat Satuan...')
        satuan_data = [
            {'nama': 'Pieces', 'singkatan': 'pcs'},
            {'nama': 'Kilogram', 'singkatan': 'kg'},
            {'nama': 'Liter', 'singkatan': 'L'},
            {'nama': 'Box', 'singkatan': 'box'},
            {'nama': 'Unit', 'singkatan': 'unit'},
        ]
        
        satuan_list = []
        for data in satuan_data:
            satuan, created = Satuan.objects.get_or_create(
                nama=data['nama'],
                defaults={'singkatan': data['singkatan']}
            )
            satuan_list.append(satuan)
            if created:
                self.stdout.write(f'  ✓ {satuan.nama}')

        # 3. Buat Gudang penyimpanan (2 gudang)
        self.stdout.write('Membuat Gudang...')
        gudang_data = [
            {'kode': 'GD-01', 'nama': 'Gudang Utama', 'alamat': 'Jl. Raya Industri No. 123'},
            {'kode': 'GD-02', 'nama': 'Gudang Cabang', 'alamat': 'Jl. Merdeka No. 45'},
        ]
        
        gudang_list = []
        for data in gudang_data:
            gudang, created = Gudang.objects.get_or_create(
                kode=data['kode'],
                defaults={'nama': data['nama'], 'alamat': data['alamat']}
            )
            gudang_list.append(gudang)
            if created:
                self.stdout.write(f'  ✓ {gudang.nama}')

        # 4. Buat Produk (25 produk, 5 per kategori)
        self.stdout.write('Membuat Produk...')
        produk_names = {
            'Elektronik': ['Smartphone Samsung A54', 'Laptop ASUS ROG', 'Mouse Wireless Logitech', 'Keyboard Mechanical', 'Headphone Sony'],
            'Fashion': ['Kaos Polos Premium', 'Celana Jeans', 'Sepatu Sneakers', 'Tas Ransel', 'Jaket Hoodie'],
            'Makanan & Minuman': ['Kopi Arabica 100gr', 'Teh Hijau Premium', 'Snack Keripik', 'Coklat Import', 'Mie Instan'],
            'Peralatan Rumah': ['Panci Set', 'Blender Philips', 'Rice Cooker', 'Vacuum Cleaner', 'Setrika Uap'],
            'Olahraga': ['Sepatu Lari Nike', 'Matras Yoga', 'Dumbbell 5kg', 'Raket Badminton', 'Bola Futsal'],
        }
        
        produk_list = []
        for kategori in kategori_list:
            if kategori.nama in produk_names:
                for nama in produk_names[kategori.nama]:
                    # Harga beli acak antara Rp 50.000 - Rp 500.000
                    harga_beli = Decimal(random.randint(50000, 500000))
                    harga_jual = harga_beli * Decimal('1.3')  # Markup 30%
                    
                    produk, created = Produk.objects.get_or_create(
                        nama=nama,
                        defaults={
                            'kategori': kategori,
                            'satuan': random.choice(satuan_list),
                            'harga_beli': harga_beli,
                            'harga_jual': harga_jual,
                            'dibuat_oleh': admin_user,
                        }
                    )
                    produk_list.append(produk)
                    if created:
                        self.stdout.write(f'  ✓ {produk.nama}')
                        
                        # Buat stok acak (10-100) di setiap gudang untuk produk ini
                        for gudang in gudang_list:
                            Stok.objects.create(
                                produk=produk,
                                gudang=gudang,
                                jumlah=random.randint(10, 100)
                            )

        # 5. Buat Customer (10 customer contoh)
        self.stdout.write('Membuat Customer...')
        customer_names = [
            'PT Maju Jaya', 'CV Berkah Sentosa', 'Toko Elektronik Jaya',
            'UD Sumber Rezeki', 'PT Teknologi Nusantara', 'Toko Bangunan Sejahtera',
            'CV Mitra Usaha', 'PT Global Trading', 'Toko Serba Ada', 'UD Makmur Jaya'
        ]
        
        customer_list = []
        for i, nama in enumerate(customer_names, 1):
            customer, created = Customer.objects.get_or_create(
                kode=f'CUST-{i:03d}',
                defaults={
                    'nama': nama,
                    'telepon': f'08{random.randint(1000000000, 9999999999)}',
                    'email': f'customer{i}@example.com',
                    'alamat': f'Jl. Customer No. {i}',
                }
            )
            customer_list.append(customer)
            if created:
                self.stdout.write(f'  ✓ {customer.nama}')

        # 6. Buat Sales Order (30 SO dalam 30 hari terakhir)
        self.stdout.write('Membuat Sales Orders...')
        today = timezone.now()
        
        for i in range(30):  # Buat 30 sales order
            # Tanggal acak dalam 30 hari terakhir
            days_ago = random.randint(0, 30)
            tanggal = today - timedelta(days=days_ago)
            
            customer = random.choice(customer_list)
            gudang = random.choice(gudang_list)
            status = random.choice(['draft', 'confirmed', 'delivered', 'completed', 'completed', 'completed'])
            
            # Buat SO tanpa memanggil calculate_total (dihitung setelah item ditambah)
            so = SalesOrder(
                customer=customer,
                gudang=gudang,
                status=status,
                dibuat_oleh=admin_user,
            )
            # Override tanggal setelah pembuatan (agar tanggal sesuai data acak)
            so.save()
            so.tanggal = tanggal
            so.save(update_fields=['tanggal'])
            
            # Tambahkan 2-5 item produk per order
            num_items = random.randint(2, 5)
            selected_products = random.sample(produk_list, min(num_items, len(produk_list)))
            
            for produk in selected_products:
                jumlah = random.randint(1, 10)
                harga_satuan = produk.harga_jual
                diskon = Decimal(random.randint(0, 10000))
                
                SalesOrderItem.objects.create(
                    sales_order=so,
                    produk=produk,
                    jumlah=jumlah,
                    harga_satuan=harga_satuan,
                    diskon=diskon,
                )
            
            # Hitung total setelah semua item ditambahkan
            so.refresh_from_db()
            so.calculate_total()
            so.save()
            
            self.stdout.write(f'  ✓ {so.nomor_so} - {customer.nama} - Rp {so.total_harga:,.0f}')

        # Tampilkan ringkasan data yang berhasil dibuat
        self.stdout.write(self.style.SUCCESS('\n=== RINGKASAN ==='))
        self.stdout.write(f'Kategori: {Kategori.objects.count()}')
        self.stdout.write(f'Satuan: {Satuan.objects.count()}')
        self.stdout.write(f'Gudang: {Gudang.objects.count()}')
        self.stdout.write(f'Produk: {Produk.objects.count()}')
        self.stdout.write(f'Stok: {Stok.objects.count()}')
        self.stdout.write(f'Customer: {Customer.objects.count()}')
        self.stdout.write(f'Sales Order: {SalesOrder.objects.count()}')
        self.stdout.write(f'Sales Order Items: {SalesOrderItem.objects.count()}')
        
        total_revenue = SalesOrder.objects.filter(
            status__in=['confirmed', 'delivered', 'completed']
        ).aggregate(total=__import__('django.db.models', fromlist=['Sum']).Sum('total_harga'))['total'] or 0
        
        self.stdout.write(self.style.SUCCESS(f'\nTotal Revenue: Rp {total_revenue:,.0f}'))
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data berhasil dibuat!'))
        self.stdout.write(self.style.SUCCESS('Silakan refresh dashboard untuk melihat data: http://127.0.0.1:8000/'))
