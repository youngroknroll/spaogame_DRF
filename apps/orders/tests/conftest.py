"""
Orders 앱 테스트 픽스처
- 공통 픽스처는 apps/conftest.py 사용
- 이 파일에는 Orders 앱 전용 픽스처만 정의
"""
import pytest
from apps.conftest import API_CART, API_CART_ITEM


@pytest.fixture
def get_cart(user_client, db):
    """장바구니 조회 헬퍼 (인증된 사용자)"""
    def _get_cart():
        return user_client.get(API_CART)
    return _get_cart


@pytest.fixture
def add_to_cart(user_client, db):
    """장바구니에 상품 추가 헬퍼 (인증된 사용자)"""
    def _add_to_cart(payload):
        return user_client.post(API_CART, payload)
    return _add_to_cart


@pytest.fixture
def update_cart_item(user_client, db):
    """장바구니 상품 수량 변경 헬퍼 (인증된 사용자)"""
    def _update_cart_item(item_id, payload):
        url = API_CART_ITEM.format(item_id=item_id)
        return user_client.patch(url, payload)
    return _update_cart_item


@pytest.fixture
def remove_from_cart(user_client, db):
    """장바구니에서 상품 제거 헬퍼 (인증된 사용자)"""
    def _remove_from_cart(item_id):
        url = API_CART_ITEM.format(item_id=item_id)
        return user_client.delete(url)
    return _remove_from_cart
