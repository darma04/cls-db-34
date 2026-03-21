import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.licenses.models import Product, Client, LicenseKey
from datetime import timedelta
from django.utils import timezone

try:
    product = Product.objects.get_or_create(code="SaaS-CORE", name="SaaS Core Software")[0]
    client = Client.objects.get_or_create(name="Master Admin", email="admin@test.com")[0]
    
    lk = LicenseKey.objects.filter(product=product, client=client).first()
    if not lk:
        lk = LicenseKey.objects.create(product=product, client=client, duration_days=3000, max_devices=10, status='active')
    else:
        lk.status = 'active'
        lk.expires_at = timezone.now() + timedelta(days=3000)
        lk.is_activated = True
        lk.save()
        
    print(f"VALID_KEY:{lk.key}")
except Exception as e:
    print(f"ERROR: {e}")
