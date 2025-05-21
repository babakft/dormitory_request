# admin_users/models.py
from django.contrib.auth.models import User
from django.db import models


class AdminProfile(models.Model):
    """Simple admin profile linked to Django's User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    admin_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True)

    # Simple permissions
    can_approve_students = models.BooleanField(default=True)
    can_manage_maintenance = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin_name} ({self.user.username})"

    class Meta:
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'