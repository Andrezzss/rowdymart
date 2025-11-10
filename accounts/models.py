from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, blank=True)
    student_id = models.CharField(max_length=30, blank=True)
    default_pickup_location = models.CharField(
        max_length=100,
        blank=True,
        help_text="e.g. Student Union, Dorm Front Desk, CS Building Lobby"
    )
    delivery_notes = models.CharField(
        max_length=255,
        blank=True,
        help_text="Short instructions for pickup or delivery drop-off."
    )
    promo_opt_in = models.BooleanField(
        default=True,
        help_text="Receive Rowdy Mart deals and promos."
    )
    order_updates_opt_in = models.BooleanField(
        default=True,
        help_text="Receive notifications about your orders."
    )

    def __str__(self):
        return f"{self.user.username} profile"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    # Only save if profile exists (handles superuser creation before signal)
    if hasattr(instance, "profile"):
        instance.profile.save()
