"""
Orders 앱 시리얼라이저
"""
from rest_framework import serializers
from .models import Cart, CartItem
from apps.products.serializers import ProductSerializer, DetailedProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """장바구니 항목 시리얼라이저 (응답용)"""
    product = ProductSerializer(read_only=True)
    detailed_product = DetailedProductSerializer(read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product", "detailed_product", "quantity", "created_at"]


class CartSerializer(serializers.ModelSerializer):
    """장바구니 시리얼라이저 (응답용)"""
    items = CartItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Cart
        fields = ["id", "items", "created_at", "updated_at"]


class CartAddSerializer(serializers.Serializer):
    """장바구니 추가 요청 시리얼라이저 (입력용) - 상품 또는 상세상품"""
    product_id = serializers.IntegerField(min_value=1, required=False, help_text="상품 ID")
    detailed_product_id = serializers.IntegerField(min_value=1, required=False, help_text="상세상품 ID")
    quantity = serializers.IntegerField(default=1, min_value=1, help_text="수량")
    
    def validate(self, attrs):
        """product_id 또는 detailed_product_id 중 하나는 필수"""
        product_id = attrs.get("product_id")
        detailed_product_id = attrs.get("detailed_product_id")
        
        if not product_id and not detailed_product_id:
            raise serializers.ValidationError(
                "product_id 또는 detailed_product_id 중 하나는 필수입니다."
            )
        
        if product_id and detailed_product_id:
            raise serializers.ValidationError(
                "product_id와 detailed_product_id 중 하나만 입력해주세요."
            )
        
        return attrs


class CartUpdateSerializer(serializers.Serializer):
    """장바구니 수량 변경 요청 시리얼라이저 (입력용)"""
    quantity = serializers.IntegerField(min_value=1, help_text="변경할 수량")
