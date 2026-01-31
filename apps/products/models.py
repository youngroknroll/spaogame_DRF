from django.db import models
from django.db.models import Avg, Count
from django.core.cache import cache
from django.conf import settings

from apps.core.models import TimeStampedModel
from apps.core.cache_utils import get_cache_key


class Menu(TimeStampedModel):
    """메뉴 모델"""
    name = models.CharField(max_length=100, verbose_name="메뉴명")

    class Meta:
        db_table = "menus"
        verbose_name = "메뉴"
        verbose_name_plural = "메뉴"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Category(TimeStampedModel):
    """카테고리 모델"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="메뉴"
    )
    name = models.CharField(max_length=100, verbose_name="카테고리명")

    class Meta:
        db_table = "categories"
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리"
        ordering = ["id"]

    def __str__(self):
        return f"{self.menu.name} - {self.name}"


class Color(TimeStampedModel):
    """색상 모델"""
    name = models.CharField(max_length=50, verbose_name="색상명")
    code = models.CharField(max_length=10, verbose_name="색상코드", help_text="예: #FF0000")

    class Meta:
        db_table = "colors"
        verbose_name = "색상"
        verbose_name_plural = "색상"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Size(TimeStampedModel):
    """사이즈 모델"""
    name = models.CharField(max_length=20, verbose_name="사이즈명")
    display_order = models.PositiveIntegerField(default=0, verbose_name="정렬순서")

    class Meta:
        db_table = "sizes"
        verbose_name = "사이즈"
        verbose_name_plural = "사이즈"
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """상품 모델"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="메뉴"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="카테고리"
    )
    name = models.CharField(max_length=200, verbose_name="상품명")
    price = models.PositiveIntegerField(verbose_name="가격")
    description = models.TextField(blank=True, verbose_name="설명")

    class Meta:
        db_table = "products"
        verbose_name = "상품"
        verbose_name_plural = "상품"
        ordering = ["id"]

    def clean(self):
        """모델 검증: 카테고리가 메뉴에 속하는지 확인"""
        from django.core.exceptions import ValidationError
        if self.menu and self.category and self.category.menu != self.menu:
            raise ValidationError(
                {"category": "선택한 카테고리는 해당 메뉴에 속해야 합니다."}
            )

    def __str__(self):
        return self.name
    
    @property
    def thumbnail_url(self):
        """메인 썸네일 URL"""
        thumbnail = self.images.filter(is_thumbnail=True).first()
        return thumbnail.image_url if thumbnail else None
    
    @property
    def posting_count(self):
        """후기 개수 (캐시 적용)"""
        cache_key = get_cache_key('product_posting_count', self.id)
        count = cache.get(cache_key)
        if count is None:
            count = self.postings.count()
            cache.set(cache_key, count, settings.CACHE_TTL["RATING"])
        return count

    @property
    def average_rating(self):
        """평균 평점 (캐시 적용)"""
        cache_key = get_cache_key('product_rating', self.id)
        rating = cache.get(cache_key)
        if rating is None:
            result = self.postings.aggregate(avg=Avg("rating"))
            rating = round(result["avg"], 1) if result["avg"] else None
            cache.set(cache_key, rating, settings.CACHE_TTL["RATING"])
        return rating
    
    def get_available_colors(self):
        """해당 상품의 사용 가능한 색상들"""
        return Color.objects.filter(
            detailed_products__product=self
        ).distinct()
    
    def get_available_sizes(self):
        """해당 상품의 사용 가능한 사이즈들"""
        return Size.objects.filter(
            detailed_products__product=self
        ).distinct()


class Image(TimeStampedModel):
    """상품 이미지 모델"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="상품"
    )
    image_url = models.URLField(verbose_name="이미지 URL")
    is_thumbnail = models.BooleanField(default=False, verbose_name="썸네일 여부")
    display_order = models.PositiveIntegerField(default=0, verbose_name="정렬순서")

    class Meta:
        db_table = "images"
        verbose_name = "이미지"
        verbose_name_plural = "이미지"
        ordering = ["-is_thumbnail", "display_order", "id"]

    def __str__(self):
        return f"{self.product.name} - {'썸네일' if self.is_thumbnail else '이미지'}"


class DetailedProduct(TimeStampedModel):
    """상세 상품 모델 (색상/사이즈 조합)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="detailed_products",
        verbose_name="상품"
    )
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="detailed_products",
        verbose_name="색상"
    )
    size = models.ForeignKey(
        Size,
        on_delete=models.CASCADE,
        related_name="detailed_products",
        verbose_name="사이즈"
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="재고")

    class Meta:
        db_table = "detailed_products"
        verbose_name = "상세 상품"
        verbose_name_plural = "상세 상품"
        unique_together = [["product", "color", "size"]]
        ordering = ["id"]

    def __str__(self):
        return f"{self.product.name} - {self.color.name}/{self.size.name}"