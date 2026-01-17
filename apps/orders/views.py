"""
Orders 앱 뷰 (CBV 방식)
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    CartAddSerializer,
    CartUpdateSerializer,
)
from apps.products.models import Product, DetailedProduct


class CartView(APIView):
    """
    장바구니 조회 및 상품 추가
    - GET: 장바구니 조회 (없으면 빈 장바구니 반환)
    - POST: 장바구니에 상품 또는 상세상품 추가
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """장바구니 조회"""
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart:
            return Response({"id": None, "items": [], "created_at": None, "updated_at": None})
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """장바구니에 상품 또는 상세상품 추가"""
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        product_id = serializer.validated_data.get('product_id')
        detailed_product_id = serializer.validated_data.get('detailed_product_id')
        quantity = serializer.validated_data['quantity']
        
        cart, _ = Cart.objects.get_or_create(user=request.user)
        
        if detailed_product_id:
            # 상세 상품 기반 추가
            detailed_product = get_object_or_404(DetailedProduct, id=detailed_product_id)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                detailed_product=detailed_product,
                defaults={'quantity': quantity}
            )
        else:
            # 기존 상품 기반 추가
            product = get_object_or_404(Product, id=product_id)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        response_serializer = CartItemSerializer(cart_item)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CartItemDetailView(generics.UpdateAPIView, generics.DestroyAPIView):
    """
    장바구니 항목 수정 및 삭제
    - PATCH: 수량 변경
    - DELETE: 항목 제거
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartUpdateSerializer
    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        """현재 사용자의 장바구니 항목만 조회"""
        return CartItem.objects.filter(cart__user=self.request.user)

    def update(self, request, *args, **kwargs):
        """수량 변경 (PATCH)"""
        cart_item = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        cart_item.quantity = serializer.validated_data['quantity']
        cart_item.save()
        
        response_serializer = CartItemSerializer(cart_item)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """항목 제거 (DELETE)"""
        cart_item = self.get_object()
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
