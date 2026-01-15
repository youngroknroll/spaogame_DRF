"""
Products 앱 테스트 픽스처
"""
import pytest
from apps.products.models import Menu, Category
from apps.conftest import API_PRODUCTS_MENUS, API_PRODUCTS_CATEGORIES


@pytest.fixture
def sample_menu(db):
    """테스트용 메뉴"""
    return Menu.objects.create(name="치킨")


@pytest.fixture
def sample_category(db, sample_menu):
    """테스트용 카테고리"""
    return Category.objects.create(menu=sample_menu, name="후라이드")


@pytest.fixture
def get_menus(api_client, db):
    """메뉴 목록 조회 헬퍼 (DB 접근 필요)"""
    def _get_menus():
        return api_client.get(API_PRODUCTS_MENUS)
    return _get_menus


@pytest.fixture
def create_menu(auth_client):
    """메뉴 등록 헬퍼 (관리자 인증)"""
    def _create_menu(payload):
        return auth_client.post(API_PRODUCTS_MENUS, payload)
    return _create_menu


@pytest.fixture
def get_categories(api_client, db):
    """카테고리 목록 조회 헬퍼 (DB 접근 필요)"""
    def _get_categories(menu_id):
        url = API_PRODUCTS_CATEGORIES.format(menu_id=menu_id)
        return api_client.get(url)
    return _get_categories


@pytest.fixture
def create_category(auth_client):
    """카테고리 등록 헬퍼 (관리자 인증)"""
    def _create_category(menu_id, payload):
        url = API_PRODUCTS_CATEGORIES.format(menu_id=menu_id)
        return auth_client.post(url, payload)
    return _create_category


@pytest.fixture
def create_product(auth_client):
    """상품 등록 헬퍼 (관리자 인증)"""
    def _create_product(payload):
        from apps.conftest import API_PRODUCTS
        return auth_client.post(API_PRODUCTS, payload)
    return _create_product
