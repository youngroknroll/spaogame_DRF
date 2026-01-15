from django.db import models


class Menu(models.Model):
    """메뉴 모델"""
    name = models.CharField(max_length=100, verbose_name="메뉴명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = "menus"
        verbose_name = "메뉴"
        verbose_name_plural = "메뉴"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Category(models.Model):
    """카테고리 모델"""
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="메뉴"
    )
    name = models.CharField(max_length=100, verbose_name="카테고리명")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = "categories"
        verbose_name = "카테고리"
        verbose_name_plural = "카테고리"
        ordering = ["id"]

    def __str__(self):
        return f"{self.menu.name} - {self.name}"


class Product(models.Model):
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        db_table = "products"
        verbose_name = "상품"
        verbose_name_plural = "상품"
        ordering = ["id"]

    def __str__(self):
        return self.name
