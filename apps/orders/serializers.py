"""
Orders 앱 시리얼라이저
"""
from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """장바구니 항목 시리얼라이저 (응답용)"""
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "created_at"]


class CartSerializer(serializers.ModelSerializer):
    """장바구니 시리얼라이저 (응답용)"""
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ["id", "items", "created_at", "updated_at"]


class CartAddSerializer(serializers.Serializer):
    """장바구니 추가 요청 시리얼라이저 (입력용)"""
    product_id = serializers.IntegerField(min_value=1, help_text="상품 ID")
    quantity = serializers.IntegerField(default=1, min_value=1, help_text="수량")


class CartUpdateSerializer(serializers.Serializer):
    """장바구니 수량 변경 요청 시리얼라이저 (입력용)"""
    quantity = serializers.IntegerField(min_value=1, help_text="변경할 수량")
