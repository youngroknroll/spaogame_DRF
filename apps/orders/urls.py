"""
Orders 앱 URL 라우팅
"""
from django.urls import path
from .views import CartView, CartItemDetailView

urlpatterns = [
    path("", CartView.as_view(), name="cart-list"),
    path("<int:item_id>/", CartItemDetailView.as_view(), name="cart-item-detail"),
]
