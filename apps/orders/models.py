"""
Orders 앱 모델 (장바구니 포함)
"""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.core.models import TimeStampedModel


class Cart(TimeStampedModel):
    """
    사용자별 장바구니
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="사용자",
    )

    class Meta:
        db_table = "carts"
        verbose_name = "장바구니"
        verbose_name_plural = "장바구니 목록"

    def __str__(self):
        return f"{self.user.email}의 장바구니"


class CartItem(TimeStampedModel):
    """
    장바구니 항목 (상품 또는 상세상품 기반)
    정확히 하나의 product 또는 detailed_product만 설정되어야 함
    """

    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="items", verbose_name="장바구니"
    )
    # 기존 상품 기반 (하위 호환성)
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, null=True, blank=True, verbose_name="상품"
    )
    # 상세 상품 기반 (색상/사이즈 포함)
    detailed_product = models.ForeignKey(
        "products.DetailedProduct",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="상세상품",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")

    class Meta:
        db_table = "cart_items"
        verbose_name = "장바구니 항목"
        verbose_name_plural = "장바구니 항목 목록"
        constraints = [
            # product와 detailed_product 중 정확히 하나만 설정되어야 함
            models.CheckConstraint(
                condition=models.Q(product__isnull=False, detailed_product__isnull=True)
                | models.Q(product__isnull=True, detailed_product__isnull=False),
                name="exactly_one_product_set",
            ),
            # 같은 cart + product 조합 중복 방지
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_cart_product",
                condition=models.Q(product__isnull=False),
            ),
            # 같은 cart + detailed_product 조합 중복 방지
            models.UniqueConstraint(
                fields=["cart", "detailed_product"],
                name="unique_cart_detailed_product",
                condition=models.Q(detailed_product__isnull=False),
            ),
        ]

    def clean(self):
        """모델 검증: 정확히 하나의 product만 설정"""
        if not self.product and not self.detailed_product:
            raise ValidationError("product 또는 detailed_product 중 적어도 하나는 필수입니다.")
        if self.product and self.detailed_product:
            raise ValidationError("product와 detailed_product 중 하나만 설정할 수 있습니다.")

    def __str__(self):
        if self.detailed_product:
            return f"{self.cart.user.email} - {self.detailed_product} ({self.quantity}개)"
        if self.product:
            return f"{self.cart.user.email} - {self.product.name} ({self.quantity}개)"
        return f"{self.cart.user.email} - 유효하지 않은 항목 ({self.quantity}개)"


class Wishlist(TimeStampedModel):
    """
    사용자별 위시리스트
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wishlist",
        verbose_name="사용자",
    )

    class Meta:
        db_table = "wishlists"
        verbose_name = "위시리스트"
        verbose_name_plural = "위시리스트 목록"

    def __str__(self):
        return f"{self.user.email}의 위시리스트"


class WishlistItem(TimeStampedModel):
    """
    위시리스트 항목
    """

    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="items", verbose_name="위시리스트"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="wishlisted_items",
        verbose_name="상품",
    )

    class Meta:
        db_table = "wishlist_items"
        verbose_name = "위시리스트 항목"
        verbose_name_plural = "위시리스트 항목 목록"
        constraints = [
            models.UniqueConstraint(fields=["wishlist", "product"], name="unique_wishlist_product")
        ]

    def __str__(self):
        return f"{self.wishlist.user.email} - {self.product.name}"
