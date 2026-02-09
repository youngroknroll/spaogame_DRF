from rest_framework import serializers

from .models import Menu, Category, Product, Color, Size, Image, DetailedProduct


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


class ColorSerializer(serializers.ModelSerializer):
    """색상 시리얼라이저"""

    class Meta:
        model = Color
        fields = ["id", "name", "code", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SizeSerializer(serializers.ModelSerializer):
    """사이즈 시리얼라이저"""

    class Meta:
        model = Size
        fields = ["id", "name", "display_order", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ImageSerializer(serializers.ModelSerializer):
    """이미지 시리얼라이저"""

    class Meta:
        model = Image
        fields = ["id", "product", "image_url", "is_thumbnail", "display_order", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class DetailedProductSerializer(serializers.ModelSerializer):
    """상세 상품 시리얼라이저"""
    color_name = serializers.CharField(source="color.name", read_only=True)
    size_name = serializers.CharField(source="size.name", read_only=True)

    class Meta:
        model = DetailedProduct
        fields = ["id", "product", "color", "color_name", "size", "size_name", "stock", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    """상품 시리얼라이저 (기본)"""
    thumbnail_url = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "menu", "category", "name", "price", "description", "thumbnail_url", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate(self, attrs):
        """카테고리가 메뉴에 속하는지 검증"""
        menu = attrs.get("menu") or (self.instance.menu if self.instance else None)
        category = attrs.get("category") or (self.instance.category if self.instance else None)

        if menu and category and category.menu != menu:
            raise serializers.ValidationError({
                "category": "선택한 카테고리는 해당 메뉴에 속해야 합니다."
            })

        return attrs


class ProductDetailSerializer(serializers.ModelSerializer):
    """상품 상세 시리얼라이저 (확장 정보 포함)"""
    thumbnail_url = serializers.CharField(read_only=True)
    colors = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()
    images = ImageSerializer(many=True, read_only=True)
    posting_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "menu", "category", "name", "price", "description",
            "thumbnail_url", "colors", "sizes", "images",
            "posting_count", "average_rating",
            "created_at", "updated_at"
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

    def get_colors(self, obj):
        """사용 가능한 색상 목록"""
        colors = obj.get_available_colors()
        return ColorSerializer(colors, many=True).data

    def get_sizes(self, obj):
        """사용 가능한 사이즈 목록"""
        sizes = obj.get_available_sizes()
        return SizeSerializer(sizes, many=True).data

    def get_posting_count(self, obj):
        """
        후기 개수 (Selector의 annotate 값 사용)
        Selector를 통해 조회하면 _posting_count가 있음.
        없으면 Model property 사용 (fallback)
        """
        if hasattr(obj, '_posting_count'):
            return obj._posting_count
        return obj.posting_count

    def get_average_rating(self, obj):
        """
        평균 평점 (Selector의 annotate 값 사용)
        Selector를 통해 조회하면 _average_rating이 있음.
        없으면 Model property 사용 (fallback)
        """
        if hasattr(obj, '_average_rating'):
            rating = obj._average_rating
            return round(rating, 1) if rating else None
        return obj.average_rating
