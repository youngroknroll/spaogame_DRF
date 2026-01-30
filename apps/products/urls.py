from django.urls import path

from . import views
from apps.postings.views import PostingCreateView

app_name = "products"

urlpatterns = [
    # 메뉴/카테고리
    path("menus/", views.MenuListCreateView.as_view(), name="menu-list-create"),
    path("menus/<int:menu_id>/categories/", views.CategoryListCreateView.as_view(), name="category-list-create"),
    
    # 색상/사이즈
    path("colors/", views.ColorListCreateView.as_view(), name="color-list-create"),
    path("sizes/", views.SizeListCreateView.as_view(), name="size-list-create"),
    
    # 상품
    path("", views.ProductListCreateView.as_view(), name="product-list-create"),
    path("<int:product_id>/", views.ProductRetrieveView.as_view(), name="product-detail"),
    
    # 상품 하위 리소스
    path("<int:product_id>/images/", views.ImageListCreateView.as_view(), name="image-list-create"),
    path("<int:product_id>/detailed/", views.DetailedProductListCreateView.as_view(), name="detailed-product-list-create"),
    path("<int:product_id>/postings/", PostingCreateView.as_view(), name="posting-create"),
]
