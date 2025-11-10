from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="home"),
    path("item/<slug:slug>/", views.item_detail, name="item_detail"),
]
