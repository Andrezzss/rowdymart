from decimal import Decimal
from catalog.models import Item
from discounts.models import DiscountCode
from django.utils import timezone

TAX_RATE = Decimal("0.0825")  # 8.25%

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = {"items": {}, "discount": None}
        self.session["cart"] = cart
        self.cart = cart

    def add(self, item_id, quantity=1, override=False):
        items = self.cart["items"]
        item = Item.objects.get(pk=item_id)
        key = str(item_id)
        if key not in items:
            items[key] = {"name": item.name, "price": str(item.current_price()), "quantity": 0}
        if override:
            items[key]["quantity"] = quantity
        else:
            items[key]["quantity"] += quantity
        if items[key]["quantity"] <= 0:
            del items[key]
        self.save()

    def remove(self, item_id):
        key = str(item_id)
        if key in self.cart["items"]:
            del self.cart["items"][key]
            self.save()

    def clear(self):
        self.session["cart"] = {"items": {}, "discount": None}
        self.cart = self.session["cart"]
        self.save()

    def set_discount(self, code_str):
        code_str = code_str.strip()
        if not code_str:
            return None
        code = DiscountCode.objects.filter(code__iexact=code_str, is_active=True).first()
        now = timezone.now()
        if not code:
            return None
        if code.starts_at and code.starts_at > now:
            return None
        if code.ends_at and code.ends_at < now:
            return None
        if code.usage_limit is not None and code.used_count >= code.usage_limit:
            return None
        self.cart["discount"] = code.code
        self.save()
        return code

    def totals(self):
        subtotal = Decimal("0.00")
        for key, row in self.cart["items"].items():
            subtotal += Decimal(row["price"]) * int(row["quantity"])

        discount_amt = Decimal("0.00")
        discount_code_obj = None

        if self.cart.get("discount"):
            discount_code_obj = DiscountCode.objects.filter(
                code__iexact=self.cart["discount"], is_active=True
            ).first()
            if discount_code_obj:
                if discount_code_obj.type == DiscountCode.PERCENT:
                    discount_amt = (subtotal * (Decimal(discount_code_obj.value) / Decimal("100"))).quantize(Decimal("0.01"))
                elif discount_code_obj.type == DiscountCode.FIXED:
                    discount_amt = Decimal(discount_code_obj.value)
                elif discount_code_obj.type == DiscountCode.FREE_SHIPPING:
                    discount_amt = Decimal("0.00")

        if discount_amt > subtotal:
            discount_amt = subtotal

        discounted = subtotal - discount_amt
        tax = (discounted * TAX_RATE).quantize(Decimal("0.01"))
        total = discounted + tax

        return {
            "subtotal": subtotal,
            "discount": discount_amt,
            "discount_code": discount_code_obj.code if discount_code_obj else None,
            "tax": tax,
            "total": total,
        }

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
