from django.urls import path
from . import views

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("confirmation/<int:order_id>/", views.confirmation, name="confirmation"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
