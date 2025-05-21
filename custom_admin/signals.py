# admin_users/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import AdminProfile


@receiver(post_save, sender=User)
def create_admin_profile(sender, instance, created, **kwargs):
    """Automatically create admin profile when a staff user is created"""
    if created and instance.is_staff:
        AdminProfile.objects.create(
            user=instance,
            admin_name=instance.get_full_name() or instance.username,
            can_approve_students=True,
            can_manage_maintenance=True
        )


@receiver(post_save, sender=User)
def save_admin_profile(sender, instance, **kwargs):
    """Save admin profile when user is saved"""
    if instance.is_staff and hasattr(instance, 'admin_profile'):
        instance.admin_profile.save()