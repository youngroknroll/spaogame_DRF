"""
Orders 앱 뷰 (CBV 방식)
"""
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem, Wishlist, WishlistItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    CartAddSerializer,
    CartUpdateSerializer,
    WishlistSerializer,
    WishlistItemSerializer,
    WishlistAddSerializer,
)
from .services import CartService, WishlistService


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
        """장바구니에 상품 추가"""
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service에 위임
        cart_item = CartService.add_item(
            user=request.user,
            **serializer.validated_data
        )

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service에 위임
        cart_item = CartService.update_item_quantity(
            user=request.user,
            item_id=kwargs['item_id'],
            quantity=serializer.validated_data['quantity']
        )

        response_serializer = CartItemSerializer(cart_item)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """항목 제거 (DELETE)"""
        # Service에 위임
        CartService.remove_item(
            user=request.user,
            item_id=kwargs['item_id']
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class WishlistView(APIView):
    """
    위시리스트 조회 및 상품 추가
    - GET: 위시리스트 조회 (없으면 빈 위시리스트 반환)
    - POST: 위시리스트에 상품 추가
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """위시리스트 조회"""
        wishlist = Wishlist.objects.filter(user=request.user).first()

        if not wishlist:
            return Response({"id": None, "items": [], "created_at": None, "updated_at": None})

        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        """위시리스트에 상품 추가"""
        serializer = WishlistAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service에 위임
        wishlist_item, created = WishlistService.add_item(
            user=request.user,
            product_id=serializer.validated_data["product_id"]
        )

        response_serializer = WishlistItemSerializer(wishlist_item)
        status_code = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(response_serializer.data, status=status_code)


class WishlistItemDetailView(generics.DestroyAPIView):
    """
    위시리스트 항목 삭제
    - DELETE: 항목 제거
    """
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "item_id"

    def get_queryset(self):
        """현재 사용자의 위시리스트 항목만 조회"""
        return WishlistItem.objects.filter(wishlist__user=self.request.user)

    def destroy(self, request, *args, **kwargs):
        """항목 제거 (DELETE)"""
        # Service에 위임
        WishlistService.remove_item(
            user=request.user,
            item_id=kwargs['item_id']
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
