"""
Model AI Assistant untuk Central License Server.
AIAssistantConfig (singleton), ChatHistory, ChatFeedback.
"""
from django.db import models
from django.contrib.auth.models import User


class AIAssistantConfig(models.Model):
    """Singleton config untuk AI Assistant."""
    PROVIDER_CHOICES = [
        ('gemini', 'Google Gemini'),
        ('openai', 'OpenAI (GPT)'),
        ('groq', 'Groq (Llama)'),
    ]

    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default='gemini', verbose_name="AI Provider")
    api_key = models.CharField(max_length=200, blank=True, verbose_name="API Key")
    model_name = models.CharField(max_length=100, blank=True, default='gemini-2.0-flash', verbose_name="Model Name")
    max_tokens = models.IntegerField(default=2048, verbose_name="Max Tokens")
    temperature = models.FloatField(default=0.7, verbose_name="Temperature")
    system_prompt = models.TextField(blank=True, verbose_name="System Prompt", default=(
        "Kamu adalah AI Assistant untuk Central License Server — sistem manajemen lisensi software. "
        "Tugasmu membantu admin mengelola lisensi produk, data klien, analisa bisnis lisensi, "
        "dan memberikan insight tentang performa penjualan lisensi. "
        "Jawab dalam Bahasa Indonesia yang profesional."
    ))
    aktif = models.BooleanField(default=True, verbose_name="Aktif")

    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diupdate_pada = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konfigurasi AI"
        verbose_name_plural = "Konfigurasi AI"

    def __str__(self):
        return f"AI Config ({self.get_provider_display()})"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class ChatHistory(models.Model):
    """Riwayat chat dengan AI."""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name="Role")
    message = models.TextField(verbose_name="Pesan")
    intent = models.CharField(max_length=50, blank=True, null=True, verbose_name="Intent Terdeteksi")
    provider = models.CharField(max_length=20, blank=True, verbose_name="Provider")
    model_used = models.CharField(max_length=100, blank=True, verbose_name="Model")
    tokens_used = models.IntegerField(default=0, verbose_name="Tokens")
    response_time = models.FloatField(default=0, verbose_name="Waktu Respon (detik)")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Riwayat Chat"
        verbose_name_plural = "Riwayat Chat"
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.role}] {self.user.username}: {self.message[:50]}..."


class ChatFeedback(models.Model):
    """Feedback user terhadap respons AI."""
    RATING_CHOICES = [
        (1, 'Buruk'), (2, 'Kurang'), (3, 'Cukup'), (4, 'Baik'), (5, 'Sangat Baik'),
    ]

    chat = models.ForeignKey(ChatHistory, on_delete=models.CASCADE, related_name='feedbacks', verbose_name="Chat")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Rating")
    komentar = models.TextField(blank=True, verbose_name="Komentar")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback Chat"
        verbose_name_plural = "Feedback Chat"

    def __str__(self):
        return f"Feedback {self.rating}/5 dari {self.user.username}"
