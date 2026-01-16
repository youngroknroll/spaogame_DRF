from django.db import models

from apps.core.models import TimeStampedModel


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

    def __str__(self):
        return self.name
