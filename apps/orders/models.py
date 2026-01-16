"""
Orders 앱 모델 (장바구니 포함)
"""
from django.db import models
from django.conf import settings

from apps.core.models import TimeStampedModel


class Cart(TimeStampedModel):
    """
    사용자별 장바구니
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="사용자"
    )

    class Meta:
        db_table = "carts"
        verbose_name = "장바구니"
        verbose_name_plural = "장바구니 목록"

    def __str__(self):
        return f"{self.user.email}의 장바구니"


class CartItem(TimeStampedModel):
    """
    장바구니 항목
    """
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="장바구니"
    )
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        verbose_name="상품"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="수량")

    class Meta:
        db_table = "cart_items"
        verbose_name = "장바구니 항목"
        verbose_name_plural = "장바구니 항목 목록"
        unique_together = [["cart", "product"]]  # 같은 상품 중복 방지

    def __str__(self):
        return f"{self.cart.user.email} - {self.product.name} ({self.quantity}개)"
