from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Menu, Category, Product
from .serializers import MenuSerializer, CategorySerializer, ProductSerializer
from apps.core.permissions import IsAdminOrReadOnly


class MenuListCreateView(generics.ListCreateAPIView):
    """
    메뉴 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None  # 메뉴는 페이지네이션 불필요


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    특정 메뉴의 카테고리 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = None  # 카테고리는 페이지네이션 불필요

    def get_queryset(self):
        """URL 파라미터의 menu_id로 필터링"""
        menu_id = self.kwargs.get("menu_id")
        return Category.objects.filter(menu_id=menu_id)

    def perform_create(self, serializer):
        """URL의 menu_id 검증 및 강제 적용"""
        url_menu_id = self.kwargs.get("menu_id")
        payload_menu_id = self.request.data.get("menu")
        
        # payload의 menu가 URL의 menu_id와 다르면 에러
        if payload_menu_id and str(payload_menu_id) != str(url_menu_id):
            raise ValidationError({
                "menu": "URL의 메뉴 ID와 일치해야 합니다."
            })
        
        serializer.save(menu_id=url_menu_id)


class ProductListCreateView(generics.ListCreateAPIView):
    """
    상품 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["menu", "category"]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["name", "price", "created_at"]
    ordering = ["id"]  # 기본 정렬


class ProductRetrieveView(generics.RetrieveAPIView):
    """
    상품 상세 조회 (공개)
    - GET: 누구나 조회 가능
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = "product_id"
