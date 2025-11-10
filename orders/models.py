from django.db import models
from django.contrib.auth.models import User
from catalog.models import Item

class Order(models.Model):
    NEW = "NEW"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELLED = "CANCELLED"

    STATUS_CHOICES = [
        (NEW, "New"),
        (PAID, "Paid"),
        (SHIPPED, "Shipped"),
        (CANCELLED, "Cancelled"),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subtotal = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    discount_code = models.CharField(max_length=30, blank=True)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=NEW)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
