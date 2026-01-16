"""
Orders 앱 URL 라우팅
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.cart_list, name="cart-list"),
    path("<int:item_id>/", views.cart_item_detail, name="cart-item-detail"),
]
