"""
Wishlist URL 라우팅
"""

from django.urls import path

from .views import WishlistItemDetailView, WishlistView

urlpatterns = [
    path("", WishlistView.as_view(), name="wishlist-list"),
    path("<int:item_id>/", WishlistItemDetailView.as_view(), name="wishlist-item-detail"),
]
