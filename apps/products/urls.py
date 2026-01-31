from django.urls import path
from django.views.decorators.cache import cache_page
from django.conf import settings

from . import views
from apps.postings.views import PostingCreateView

app_name = "products"

urlpatterns = [
    # 메뉴/카테고리 (cache_page 적용)
    path("menus/", cache_page(settings.CACHE_TTL["MENU"])(views.MenuListCreateView.as_view()), name="menu-list-create"),
    path("menus/<int:menu_id>/categories/", cache_page(settings.CACHE_TTL["CATEGORY"])(views.CategoryListCreateView.as_view()), name="category-list-create"),

    # 색상/사이즈 (cache_page 적용)
    path("colors/", cache_page(settings.CACHE_TTL["CATEGORY"])(views.ColorListCreateView.as_view()), name="color-list-create"),
    path("sizes/", cache_page(settings.CACHE_TTL["CATEGORY"])(views.SizeListCreateView.as_view()), name="size-list-create"),

    # 상품 (cache_page 적용)
    path("", cache_page(settings.CACHE_TTL["PRODUCT_LIST"])(views.ProductListCreateView.as_view()), name="product-list-create"),
    path("<int:product_id>/", cache_page(settings.CACHE_TTL["PRODUCT_DETAIL"])(views.ProductRetrieveView.as_view()), name="product-detail"),

    # 상품 하위 리소스 (cache_page 적용)
    path("<int:product_id>/images/", cache_page(settings.CACHE_TTL["PRODUCT_DETAIL"])(views.ImageListCreateView.as_view()), name="image-list-create"),
    path("<int:product_id>/detailed/", cache_page(settings.CACHE_TTL["STOCK"])(views.DetailedProductListCreateView.as_view()), name="detailed-product-list-create"),
    path("<int:product_id>/postings/", PostingCreateView.as_view(), name="posting-create"),
]
