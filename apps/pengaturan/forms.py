from django import forms
from .models import PengaturanPerusahaan

class PengaturanPerusahaanForm(forms.ModelForm):
    class Meta:
        model = PengaturanPerusahaan
        fields = '__all__'
