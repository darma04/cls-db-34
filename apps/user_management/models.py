"""
==========================================================================
 USER MANAGEMENT MODELS - Import Model dari Auth Module
==========================================================================
 User management tidak memiliki models sendiri karena:
 - Data user disimpan di django.contrib.auth.models.User (bawaan Django)
 - Data profil (role, foto) disimpan di auth.models.Profile
 - Module ini hanya menyediakan views untuk CRUD user

 Import Profile di sini agar bisa digunakan oleh views.py
 tanpa harus import langsung dari 'auth.models' setiap kali.
==========================================================================
"""
# Import Profile dari modul auth untuk digunakan di views
from auth.models import Profile
