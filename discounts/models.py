from django.db import models

class DiscountCode(models.Model):
    PERCENT = "PERCENT"
    FIXED = "FIXED"
    FREE_SHIPPING = "FREE_SHIPPING"

    TYPE_CHOICES = [
        (PERCENT, "Percent"),
        (FIXED, "Fixed Amount"),
        (FREE_SHIPPING, "Free Shipping"),
    ]

    code = models.CharField(max_length=30, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    value = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
