from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
    path("menus/", views.MenuListCreateView.as_view(), name="menu-list-create"),
    path("menus/<int:menu_id>/categories/", views.CategoryListCreateView.as_view(), name="category-list-create"),
    path("", views.ProductListCreateView.as_view(), name="product-list-create"),
]
