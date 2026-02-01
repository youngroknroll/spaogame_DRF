"""
Product 앱 시그널
캐시 무효화 로직
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from apps.core.cache_utils import invalidate_cache


@receiver([post_save, post_delete], sender='postings.Posting')
def invalidate_product_rating_cache(sender, instance, **kwargs):
    """
    후기(Posting)가 생성/수정/삭제될 때 해당 상품의 평점 캐시 무효화
    """
    if hasattr(instance, 'product') and instance.product:
        product_id = instance.product.id
        invalidate_cache('product_rating', product_id)
        invalidate_cache('product_posting_count', product_id)


@receiver([post_save, post_delete], sender='products.DetailedProduct')
def invalidate_stock_cache(sender, instance, **kwargs):
    """
    DetailedProduct(재고)가 변경될 때 캐시 무효화
    """
    if hasattr(instance, 'id'):
        invalidate_cache('detailed_product_stock', instance.id)
