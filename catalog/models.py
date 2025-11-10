from django.db import models
from django.utils.text import slugify

class Item(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="items/", null=True, blank=True)
    category = models.CharField(max_length=60, blank=True)
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def current_price(self):
        if self.is_on_sale and self.sale_price is not None:
            return self.sale_price
        return self.price

    def __str__(self):
        return self.name
