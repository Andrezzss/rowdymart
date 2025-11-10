from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from .models import Item

def item_list(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "")
    items = Item.objects.all()

    if q:
        items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if sort == "price_asc":
        items = items.order_by("price")
    elif sort == "price_desc":
        items = items.order_by("-price")
    elif sort == "availability":
        items = items.order_by("-quantity_available")

    return render(request, "catalog/list.html", {"items": items, "q": q, "sort": sort})

def item_detail(request, slug):
    item = get_object_or_404(Item, slug=slug)
    return render(request, "catalog/detail.html", {"item": item})
