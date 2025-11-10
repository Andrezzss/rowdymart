from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render

from cart.cart import Cart
from catalog.models import Item
from discounts.models import DiscountCode
from .models import Order, OrderItem


@login_required
@transaction.atomic
def checkout(request):
    cart = Cart(request)
    if not cart.cart["items"]:
        messages.error(request, "Your cart is empty.")
        return redirect("home")

    totals = cart.totals()

    # Validate inventory with row locking
    items_map = {}
    for key, row in cart.cart["items"].items():
        item = Item.objects.select_for_update().get(pk=int(key))
        qty = int(row["quantity"])
        if qty > item.quantity_available:
            messages.error(request, f"Not enough stock for {item.name}.")
            return redirect("view_cart")
        items_map[item.id] = (item, qty, Decimal(row["price"]))

    discount_code_str = cart.cart.get("discount") or ""

    order = Order.objects.create(
        user=request.user,
        subtotal=totals["subtotal"],
        discount=totals["discount"],
        tax=totals["tax"],
        total=totals["total"],
        discount_code=discount_code_str,
    )

    for item_id, (item, qty, price) in items_map.items():
        OrderItem.objects.create(
            order=order,
            item=item,
            name=item.name,
            price=price,
            quantity=qty,
        )
        item.quantity_available = max(0, item.quantity_available - qty)
        item.save()

    if discount_code_str:
        code = DiscountCode.objects.select_for_update().filter(code__iexact=discount_code_str).first()
        if code:
            code.used_count = F("used_count") + 1
            code.save()

    cart.clear()
    messages.success(request, "Order placed successfully.")
    return redirect("confirmation", order_id=order.id)


@login_required
def confirmation(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, "You do not have access to this order.")
        return redirect("home")
    return render(request, "orders/confirmation.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders/my_orders.html", {"orders": orders})
