# dashboard/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.shortcuts import render

from orders.models import Order
from catalog.models import Item

@staff_member_required
def index(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum("total"))["total"] or 0
    recent_orders = Order.objects.select_related("user").order_by("-created_at")[:5]
    # Fix: filter first, then slice
    low_stock_items = Item.objects.filter(quantity_available__lte=5).order_by("quantity_available")[:10]

    context = {
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_items": low_stock_items,
    }
    return render(request, "dashboard/index.html", context)
