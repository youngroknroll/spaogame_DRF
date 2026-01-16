"""
Products 앱 테스트 픽스처
"""
import pytest
from apps.products.models import Menu, Category, Product
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
def sample_products(db, sample_menu, sample_category):
    """테스트용 상품들"""
    products = [
        Product.objects.create(
            menu=sample_menu,
            category=sample_category,
            name="후라이드치킨",
            price=18000,
            description="바삭한 후라이드치킨"
        ),
        Product.objects.create(
            menu=sample_menu,
            category=sample_category,
            name="양념치킨",
            price=19000,
            description="달콤한 양념치킨"
        )
    ]
    return products


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


@pytest.fixture
def create_product_as_user(user_client):
    """상품 등록 헬퍼 (일반 사용자 인증)"""
    def _create_product(payload):
        from apps.conftest import API_PRODUCTS
        return user_client.post(API_PRODUCTS, payload)
    return _create_product


@pytest.fixture
def get_products(api_client, db):
    """상품 목록 조회 헬퍼 (DB 접근 필요)"""
    def _get_products(menu_id=None, category_id=None):
        from apps.conftest import API_PRODUCTS
        params = {}
        if menu_id:
            params["menu"] = menu_id
        if category_id:
            params["category"] = category_id
        return api_client.get(API_PRODUCTS, params)
    return _get_products


@pytest.fixture
def get_product_detail(api_client, db):
    """상품 상세 조회 헬퍼 (DB 접근 필요)"""
    def _get_product_detail(product_id):
        from apps.conftest import API_PRODUCT_DETAIL
        url = API_PRODUCT_DETAIL.format(product_id=product_id)
        return api_client.get(url)
    return _get_product_detail
