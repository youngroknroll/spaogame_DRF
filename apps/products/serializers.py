from rest_framework import serializers

from .models import Menu, Category, Product


class MenuSerializer(serializers.ModelSerializer):
    """메뉴 시리얼라이저"""
    
    class Meta:
        model = Menu
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class CategorySerializer(serializers.ModelSerializer):
    """카테고리 시리얼라이저"""
    
    class Meta:
        model = Category
        fields = ["id", "menu", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    """상품 시리얼라이저"""
    
    class Meta:
        model = Product
        fields = ["id", "menu", "category", "name", "price", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
    
    def validate(self, attrs):
        """카테고리가 메뉴에 속하는지 검증"""
        menu = attrs.get("menu")
        category = attrs.get("category")
        
        if menu and category and category.menu != menu:
            raise serializers.ValidationError({
                "category": "카테고리는 선택한 메뉴에 속해야 합니다."
            })
        
        return attrs
