"""
Orders 앱 테스트 픽스처
- 공통 픽스처는 apps/conftest.py 사용
- 이 파일에는 Orders 앱 전용 픽스처만 정의
"""
import pytest
from apps.conftest import API_CART, API_CART_ITEM, API_WISHLIST, API_WISHLIST_ITEM


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


# ============================================================
# 상세 상품 기반 장바구니 Fixtures
# ============================================================

@pytest.fixture
def sample_detailed_product_for_cart(db, sample_menu, sample_category):
    """장바구니 테스트용 상세 상품"""
    from apps.products.models import Product, Color, Size, DetailedProduct
    
    product = Product.objects.create(
        menu=sample_menu,
        category=sample_category,
        name="장바구니 테스트 상품",
        price=25000,
        description="테스트용 상품"
    )
    
    color = Color.objects.create(name="블랙", code="#000000")
    size = Size.objects.create(name="M", display_order=2)
    
    detailed_product = DetailedProduct.objects.create(
        product=product,
        color=color,
        size=size,
        stock=100
    )
    
    return detailed_product


@pytest.fixture
def add_detailed_to_cart(user_client, db):
    """상세 상품을 장바구니에 추가하는 헬퍼 (인증된 사용자)"""
    def _add_detailed_to_cart(payload):
        return user_client.post(API_CART, payload)
    return _add_detailed_to_cart


@pytest.fixture
def get_wishlist(user_client, db):
    """위시리스트 조회 헬퍼 (인증된 사용자)"""
    def _get_wishlist():
        return user_client.get(API_WISHLIST)
    return _get_wishlist


@pytest.fixture
def add_to_wishlist(user_client, db):
    """위시리스트에 상품 추가 헬퍼 (인증된 사용자)"""
    def _add_to_wishlist(payload):
        return user_client.post(API_WISHLIST, payload)
    return _add_to_wishlist


@pytest.fixture
def remove_from_wishlist(user_client, db):
    """위시리스트에서 상품 제거 헬퍼 (인증된 사용자)"""
    def _remove_from_wishlist(item_id):
        url = API_WISHLIST_ITEM.format(item_id=item_id)
        return user_client.delete(url)
    return _remove_from_wishlist


@pytest.fixture
def get_wishlist_anonymous(api_client):
    """위시리스트 조회 헬퍼 (비인증 사용자)"""
    def _get_wishlist_anonymous():
        return api_client.get(API_WISHLIST)
    return _get_wishlist_anonymous


@pytest.fixture
def add_to_wishlist_anonymous(api_client):
    """위시리스트 추가 헬퍼 (비인증 사용자)"""
    def _add_to_wishlist_anonymous(payload):
        return api_client.post(API_WISHLIST, payload)
    return _add_to_wishlist_anonymous


@pytest.fixture
def remove_from_wishlist_anonymous(api_client):
    """위시리스트 삭제 헬퍼 (비인증 사용자)"""
    def _remove_from_wishlist_anonymous(item_id):
        url = API_WISHLIST_ITEM.format(item_id=item_id)
        return api_client.delete(url)
    return _remove_from_wishlist_anonymous


@pytest.fixture
def wishlist_item(db, regular_user, sample_product):
    """위시리스트 항목 (비인증 테스트용)"""
    from apps.orders.models import Wishlist, WishlistItem

    wishlist = Wishlist.objects.create(user=regular_user)
    return WishlistItem.objects.create(wishlist=wishlist, product=sample_product)
