"""
공통 추상 모델
"""
from django.db import models


class TimeStampedModel(models.Model):
    """
    created_at, updated_at 필드를 제공하는 추상 모델
    모든 도메인 모델에서 상속하여 사용
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="생성일시")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일시")

    class Meta:
        abstract = True
