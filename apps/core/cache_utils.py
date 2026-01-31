"""
캐시 유틸리티 함수
키 기반 캐싱을 위한 헬퍼 함수들
"""
from django.core.cache import cache
from django.conf import settings
from functools import wraps


def get_cache_key(prefix, *args):
    """
    캐시 키 생성

    Args:
        prefix: 캐시 키 접두사
        *args: 추가 식별자

    Returns:
        str: 생성된 캐시 키
    """
    parts = [str(arg) for arg in args if arg is not None]
    return f"{prefix}:{'_'.join(parts)}"


def cache_decorator(key_prefix, timeout_key):
    """
    함수 결과를 캐싱하는 데코레이터

    Args:
        key_prefix: 캐시 키 접두사
        timeout_key: settings.CACHE_TTL의 키
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # self가 있는 경우 (메서드) id를 키에 포함
            cache_key_parts = [key_prefix]
            if args and hasattr(args[0], 'id'):
                cache_key_parts.append(str(args[0].id))

            cache_key = get_cache_key(*cache_key_parts)

            # 캐시에서 조회
            result = cache.get(cache_key)
            if result is not None:
                return result

            # 캐시 미스: 함수 실행 및 캐시에 저장
            result = func(*args, **kwargs)
            timeout = settings.CACHE_TTL.get(timeout_key, 300)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper
    return decorator


def invalidate_cache(key_prefix, *identifiers):
    """
    특정 캐시 키 무효화

    Args:
        key_prefix: 캐시 키 접두사
        *identifiers: 추가 식별자
    """
    cache_key = get_cache_key(key_prefix, *identifiers)
    cache.delete(cache_key)


def invalidate_pattern(pattern):
    """
    패턴에 맞는 모든 캐시 무효화

    Args:
        pattern: 캐시 키 패턴 (예: "product_rating:*")

    Note:
        LocMemCache는 패턴 삭제를 지원하지 않으므로,
        Redis 등으로 변경 시 구현 필요
    """
    # LocMemCache는 패턴 삭제 미지원
    # Redis 사용 시: cache.delete_pattern(pattern)
    pass
