"""
Orders 앱 시리얼라이저
"""
from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """장바구니 항목 시리얼라이저"""
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "created_at"]


class CartSerializer(serializers.ModelSerializer):
    """장바구니 시리얼라이저"""
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ["id", "items", "created_at", "updated_at"]
