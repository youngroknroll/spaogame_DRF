"""
Postings 앱 모델 (후기 및 댓글)
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.core.models import TimeStampedModel


class Posting(TimeStampedModel):
    """
    상품 후기
    """
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="postings",
        verbose_name="상품"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="postings",
        verbose_name="작성자"
    )
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="평점"
    )

    class Meta:
        db_table = "postings"
        verbose_name = "후기"
        verbose_name_plural = "후기 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.name} - {self.title}"


class Comment(TimeStampedModel):
    """
    후기에 대한 댓글
    """
    posting = models.ForeignKey(
        Posting,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="후기"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="작성자"
    )
    content = models.TextField(verbose_name="내용")

    class Meta:
        db_table = "comments"
        verbose_name = "댓글"
        verbose_name_plural = "댓글 목록"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.posting.title} - {self.user.email}"
