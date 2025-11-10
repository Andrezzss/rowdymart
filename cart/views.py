from decimal import Decimal
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from catalog.models import Item
from .cart import Cart
from .forms import ApplyDiscountForm


def view_cart(request):
    cart = Cart(request)
    items = []
    for key, row in cart.cart["items"].items():
        price = Decimal(row["price"])
        quantity = int(row["quantity"])
        line_total = price * quantity
        items.append({
            "id": int(key),
            "name": row["name"],
            "price": price,
            "quantity": quantity,
            "line_total": line_total,
        })
    totals = cart.totals()
    form = ApplyDiscountForm()
    return render(request, "cart/cart.html", {"items": items, "totals": totals, "form": form})


def add_to_cart(request):
    if request.method == "POST":
        item_id = int(request.POST.get("item_id"))
        quantity = int(request.POST.get("quantity", 1))
        item = get_object_or_404(Item, pk=item_id)
        if quantity > item.quantity_available:
            messages.error(request, "Not enough inventory available.")
            return redirect("item_detail", slug=item.slug)
        cart = Cart(request)
        cart.add(item_id, quantity)
        messages.success(request, "Added to cart.")
    return redirect("view_cart")


def update_quantity(request, item_id):
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity < 1:
            quantity = 1
        item = get_object_or_404(Item, pk=item_id)
        if quantity > item.quantity_available:
            messages.error(request, "Not enough inventory available.")
            return redirect("view_cart")
        cart = Cart(request)
        cart.add(item_id, quantity, override=True)
        messages.success(request, "Quantity updated.")
    return redirect("view_cart")


def remove_from_cart(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    messages.info(request, "Removed from cart.")
    return redirect("view_cart")


def apply_discount(request):
    if request.method == "POST":
        form = ApplyDiscountForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data["code"]
            cart = Cart(request)
            if cart.set_discount(code):
                messages.success(request, "Discount applied.")
            else:
                messages.error(request, "Invalid or inactive discount code.")
    return redirect("view_cart")
