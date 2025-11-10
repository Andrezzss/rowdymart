from django.contrib import admin
from .models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "quantity_available", "is_on_sale", "sale_price", "category")
    list_filter = ("is_on_sale", "category")
    search_fields = ("name", "description")
    ordering = ("name",)
