from django.contrib import admin
from .models import DiscountCode

@admin.register(DiscountCode)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "value", "is_active", "used_count", "usage_limit", "starts_at", "ends_at")
    list_filter = ("type", "is_active")
    search_fields = ("code",)
