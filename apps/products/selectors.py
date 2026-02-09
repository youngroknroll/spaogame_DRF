"""
Products 도메인 조회 로직

Selector Layer는 조회 로직을 분리하고 N+1 쿼리를 최적화합니다.
"""

from django.db.models import Avg, Count, Prefetch
from django.shortcuts import get_object_or_404

from .models import Category, DetailedProduct, Image, Menu, Product


class ProductSelector:
    """상품 조회 로직"""

    @staticmethod
    def get_product_list(menu_id=None, category_id=None):
        """
        상품 목록 조회 (N+1 최적화)

        Args:
            menu_id: 메뉴 ID 필터
            category_id: 카테고리 ID 필터

        Returns:
            QuerySet: 최적화된 상품 쿼리셋
        """
        qs = Product.objects.all()

        # 필터링
        if menu_id:
            qs = qs.filter(menu_id=menu_id)
        if category_id:
            qs = qs.filter(category_id=category_id)

        # N+1 최적화: 통계 정보를 한 번에 조회
        qs = (
            qs.annotate(
                _posting_count=Count("postings", distinct=True),
                _average_rating=Avg("postings__rating"),
            )
            .select_related("menu", "category")
            .prefetch_related(
                Prefetch(
                    "images",
                    queryset=Image.objects.filter(is_thumbnail=True),
                    to_attr="thumbnail_images",
                )
            )
        )

        return qs

    @staticmethod
    def get_product_detail(product_id):
        """
        상품 상세 조회 (연관 데이터 prefetch)

        Args:
            product_id: 상품 ID

        Returns:
            Product: 상품 객체 (연관 데이터 포함)
        """
        queryset = (
            Product.objects.annotate(
                _posting_count=Count("postings", distinct=True),
                _average_rating=Avg("postings__rating"),
            )
            .select_related("menu", "category")
            .prefetch_related(
                "images",
                Prefetch(
                    "detailed_products",
                    queryset=DetailedProduct.objects.select_related("color", "size"),
                ),
                "postings__user",
                "postings__comments__user",
            )
        )

        return get_object_or_404(queryset, id=product_id)

    @staticmethod
    def get_products_with_thumbnail():
        """
        메인 페이지용 상품 목록 (썸네일 포함)

        Returns:
            QuerySet: 썸네일이 있는 상품 목록
        """
        return Product.objects.prefetch_related(
            Prefetch(
                "images",
                queryset=Image.objects.filter(is_thumbnail=True),
                to_attr="thumbnail_images",
            )
        ).annotate(_posting_count=Count("postings", distinct=True))


class MenuSelector:
    """메뉴 조회 로직"""

    @staticmethod
    def get_all_menus():
        """
        메뉴 목록 조회

        Returns:
            QuerySet: 전체 메뉴 목록
        """
        return Menu.objects.all()

    @staticmethod
    def get_menu_with_categories(menu_id):
        """
        메뉴와 카테고리 목록 조회 (한 번의 쿼리)

        Args:
            menu_id: 메뉴 ID

        Returns:
            Menu: 메뉴 객체 (카테고리 포함)
        """
        return get_object_or_404(Menu.objects.prefetch_related("categories"), id=menu_id)

    @staticmethod
    def get_categories_by_menu(menu_id):
        """
        특정 메뉴의 카테고리 목록

        Args:
            menu_id: 메뉴 ID

        Returns:
            QuerySet: 카테고리 목록
        """
        return Category.objects.filter(menu_id=menu_id)
