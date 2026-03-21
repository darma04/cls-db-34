"""
Model UserActivity untuk audit trail di Central License Server.
Mencatat semua aktivitas user: login, logout, create, update, delete.
"""
import json
from django.db import models
from django.contrib.auth.models import User


class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('export', 'Export'),
        ('import', 'Import'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('activate', 'Aktivasi Lisensi'),
        ('suspend', 'Suspend Lisensi'),
        ('view', 'View'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="Aksi")
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Model")
    object_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Object ID")
    object_repr = models.CharField(max_length=200, blank=True, null=True, verbose_name="Object Repr")
    description = models.TextField(blank=True, null=True, verbose_name="Deskripsi")
    changes = models.TextField(blank=True, null=True, verbose_name="Perubahan (JSON)")

    ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="IP Address")
    user_agent = models.CharField(max_length=500, blank=True, null=True, verbose_name="User Agent")
    request_path = models.CharField(max_length=500, blank=True, null=True, verbose_name="Request Path")
    request_method = models.CharField(max_length=10, blank=True, null=True, verbose_name="HTTP Method")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Waktu")

    class Meta:
        verbose_name = "Aktivitas User"
        verbose_name_plural = "Aktivitas User"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['action']),
        ]

    def __str__(self):
        username = self.user.username if self.user else 'System'
        return f"[{self.action}] {username} - {self.description or self.model_name or ''}"

    def get_changes_dict(self):
        if self.changes:
            try:
                return json.loads(self.changes)
            except (json.JSONDecodeError, ValueError):
                return {}
        return {}

    def set_changes(self, changes_dict):
        from django.core.serializers.json import DjangoJSONEncoder
        self.changes = json.dumps(changes_dict, cls=DjangoJSONEncoder)
