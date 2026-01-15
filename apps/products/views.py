from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Menu, Category, Product
from .serializers import MenuSerializer, CategorySerializer, ProductSerializer


class MenuListCreateView(generics.ListCreateAPIView):
    """
    메뉴 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_permissions(self):
        """HTTP 메서드에 따라 권한 분기"""
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


class CategoryListCreateView(generics.ListCreateAPIView):
    """
    특정 메뉴의 카테고리 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    serializer_class = CategorySerializer

    def get_queryset(self):
        """URL 파라미터의 menu_id로 필터링"""
        menu_id = self.kwargs.get("menu_id")
        return Category.objects.filter(menu_id=menu_id)

    def get_permissions(self):
        """HTTP 메서드에 따라 권한 분기"""
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]


class ProductListCreateView(generics.ListCreateAPIView):
    """
    상품 목록 조회 (공개) 및 등록 (관리자)
    - GET: 누구나 조회 가능
    - POST: 관리자만 등록 가능
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        """HTTP 메서드에 따라 권한 분기"""
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [AllowAny()]
