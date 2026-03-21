"""
==========================================================================
 NORMALIZE PERMISSIONS - Management Command Normalisasi Database Permission
==========================================================================
 Perintah CLI untuk menormalisasi format data permission di database:
 1. Nama modul → lowercase (contoh: "Produk" → "produk")
 2. Nama sub_modul → lowercase, hapus prefix jika ada dash
    (contoh: "produk-kategori" → "kategori", "Kategori" → "kategori")

 Cara pakai:
   python manage.py normalize_permissions            # Eksekusi langsung
   python manage.py normalize_permissions --dry-run   # Preview saja (tanpa ubah DB)

 Mengapa diperlukan:
 - Saat user membuat role/permission via UI, bisa saja case-nya tidak konsisten
 - Sidebar menggunakan lowercase untuk pencocokan permission
 - Normalisasi memastikan semua pencocokan berjalan benar

 Terhubung dengan:
 - core/models.py → RolePermission (model yang dinormalisasi)
==========================================================================
"""

from django.core.management.base import BaseCommand
from apps.core.models import RolePermission


class Command(BaseCommand):
    """
    Management command untuk normalisasi format data permission di database.

    Mengubah semua nama modul dan sub-modul ke lowercase untuk memastikan
    konsistensi pencocokan di sidebar dan pengecekan permission.

    Cara pakai:
      python manage.py normalize_permissions            # Eksekusi langsung
      python manage.py normalize_permissions --dry-run   # Preview saja
    """
    help = 'Normalize Permission database format: lowercase module/sub_module names'

    def add_arguments(self, parser):
        """Tambahkan argumen command line untuk management command."""
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually modifying database',
        )

    def handle(self, *args, **options):
        """Logika utama management command — dipanggil saat command dijalankan."""
        dry_run = options['dry_run']
        
        self.stdout.write(self.style.WARNING('\n' + '='*70))
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        else:
            self.stdout.write(self.style.WARNING('LIVE MODE - Database will be modified!'))
        self.stdout.write(self.style.WARNING('='*70 + '\n'))
        
        permissions = RolePermission.objects.all()
        total = permissions.count()
        modified_count = 0
        
        self.stdout.write(f'Found {total} permission records to check...\n')
        
        for perm in permissions:
            original_module = perm.module
            original_sub_module = perm.sub_module
            modified = False
            
            # Normalize module to lowercase
            if perm.module:
                normalized_module = perm.module.lower().strip()
                if perm.module != normalized_module:
                    self.stdout.write(f'  Module: "{perm.module}" -> "{normalized_module}"')
                    perm.module = normalized_module
                    modified = True
            
            # Normalize sub_module:
            # 1. Ekstrak bagian setelah dash jika ada
            # 2. Konversi ke huruf kecil (lowercase)
            if perm.sub_module:
                sub_normalized = perm.sub_module.lower().strip()
                
                # Jika mengandung dash, ambil bagian setelah dash pertama
                # contoh: "produk-kategori" -> "kategori"
                if '-' in sub_normalized:
                    parts = sub_normalized.split('-', 1)
                    if len(parts) > 1:
                        sub_normalized = parts[1]
                
                if perm.sub_module != sub_normalized:
                    self.stdout.write(f'  SubModule: "{perm.sub_module}" -> "{sub_normalized}"')
                    perm.sub_module = sub_normalized
                    modified = True
            
            if modified:
                role_display = perm.get_role_display() if hasattr(perm, 'get_role_display') else perm.role
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ [{role_display}] '
                        f'{original_module or "N/A"} / {original_sub_module or "N/A"}'
                    )
                )
                
                if not dry_run:
                    perm.save()
                
                modified_count += 1
        
        self.stdout.write('\n' + '='*70)
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'\nDRY RUN COMPLETE: Would modify {modified_count} of {total} permissions'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    '\nRun without --dry-run to apply changes'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n✓ NORMALIZATION COMPLETE: Modified {modified_count} of {total} permissions'
                )
            )
            if modified_count > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        '\nPermission database normalized successfully!'
                    )
                )
                self.stdout.write(
                    'Please refresh your browser to see updated sidebar filtering.\n'
                )
        self.stdout.write('='*70 + '\n')
