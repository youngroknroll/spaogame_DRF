"""
Products 앱 테스트 픽스처
- 공통 픽스처(sample_menu, sample_category, sample_product)는 apps/conftest.py 사용
- 이 파일에는 Products 앱 전용 픽스처만 정의
"""

import pytest

from apps.conftest import (
    API_COLORS,
    API_DETAILED_PRODUCTS,
    API_IMAGES,
    API_PRODUCT_DETAIL,
    API_PRODUCTS,
    API_PRODUCTS_CATEGORIES,
    API_PRODUCTS_MENUS,
    API_SIZES,
)
from apps.products.models import Product


@pytest.fixture
def sample_products(db, sample_menu, sample_category):
    """테스트용 상품들 (여러 개 - Products 앱 전용)"""
    products = [
        Product.objects.create(
            menu=sample_menu,
            category=sample_category,
            name="후라이드치킨",
            price=18000,
            description="바삭한 후라이드치킨",
        ),
        Product.objects.create(
            menu=sample_menu,
            category=sample_category,
            name="양념치킨",
            price=19000,
            description="달콤한 양념치킨",
        ),
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
        return auth_client.post(API_PRODUCTS, payload)

    return _create_product


@pytest.fixture
def create_product_as_user(user_client):
    """상품 등록 헬퍼 (일반 사용자 인증)"""

    def _create_product(payload):
        return user_client.post(API_PRODUCTS, payload)

    return _create_product


@pytest.fixture
def get_products(api_client, db):
    """상품 목록 조회 헬퍼 (DB 접근 필요)"""

    def _get_products(menu_id=None, category_id=None):
        params = {}
        if menu_id:
            params["menu"] = menu_id
        if category_id:
            params["category"] = category_id
        return api_client.get(API_PRODUCTS, params)

    return _get_products


@pytest.fixture
def get_products_with_ordering(api_client, db):
    """상품 목록 조회 헬퍼 - 정렬 지원 (DB 접근 필요)"""

    def _get_products(menu_id=None, category_id=None, ordering=None):
        params = {}
        if menu_id:
            params["menu"] = menu_id
        if category_id:
            params["category"] = category_id
        if ordering:
            params["ordering"] = ordering
        return api_client.get(API_PRODUCTS, params)

    return _get_products


@pytest.fixture
def get_product_detail(api_client, db):
    """상품 상세 조회 헬퍼 (DB 접근 필요)"""

    def _get_product_detail(product_id):
        url = API_PRODUCT_DETAIL.format(product_id=product_id)
        return api_client.get(url)

    return _get_product_detail


# ============================================================
# 상세 도메인 Fixtures (Color, Size, Image, DetailedProduct)
# ============================================================


@pytest.fixture
def create_color(auth_client):
    """색상 등록 헬퍼 (관리자 인증)"""

    def _create_color(payload):
        return auth_client.post(API_COLORS, payload)

    return _create_color


@pytest.fixture
def get_colors(api_client, db):
    """색상 목록 조회 헬퍼"""

    def _get_colors():
        return api_client.get(API_COLORS)

    return _get_colors


@pytest.fixture
def sample_colors(db):
    """테스트용 색상들"""
    from apps.products.models import Color

    return [
        Color.objects.create(name="레드", code="#FF0000"),
        Color.objects.create(name="블루", code="#0000FF"),
    ]


@pytest.fixture
def create_size(auth_client):
    """사이즈 등록 헬퍼 (관리자 인증)"""

    def _create_size(payload):
        return auth_client.post(API_SIZES, payload)

    return _create_size


@pytest.fixture
def get_sizes(api_client, db):
    """사이즈 목록 조회 헬퍼"""

    def _get_sizes():
        return api_client.get(API_SIZES)

    return _get_sizes


@pytest.fixture
def sample_sizes(db):
    """테스트용 사이즈들"""
    from apps.products.models import Size

    return [
        Size.objects.create(name="S", display_order=1),
        Size.objects.create(name="M", display_order=2),
        Size.objects.create(name="L", display_order=3),
    ]


@pytest.fixture
def create_image(auth_client):
    """이미지 등록 헬퍼 (관리자 인증)"""

    def _create_image(payload):
        product_id = payload.get("product")
        url = API_IMAGES.format(product_id=product_id)
        return auth_client.post(url, payload)

    return _create_image


@pytest.fixture
def get_images(api_client, db):
    """이미지 목록 조회 헬퍼"""

    def _get_images(product_id):
        url = API_IMAGES.format(product_id=product_id)
        return api_client.get(url)

    return _get_images


@pytest.fixture
def sample_images(db, sample_product):
    """테스트용 이미지들"""
    from apps.products.models import Image

    return [
        Image.objects.create(
            product=sample_product, image_url="https://example.com/thumb.jpg", is_thumbnail=True
        ),
        Image.objects.create(
            product=sample_product, image_url="https://example.com/detail.jpg", is_thumbnail=False
        ),
    ]


@pytest.fixture
def create_detailed_product(auth_client):
    """상세 상품 등록 헬퍼 (관리자 인증)"""

    def _create_detailed_product(payload):
        product_id = payload.get("product")
        url = API_DETAILED_PRODUCTS.format(product_id=product_id)
        return auth_client.post(url, payload)

    return _create_detailed_product


@pytest.fixture
def get_detailed_products(api_client, db):
    """상세 상품 목록 조회 헬퍼"""

    def _get_detailed_products(product_id):
        url = API_DETAILED_PRODUCTS.format(product_id=product_id)
        return api_client.get(url)

    return _get_detailed_products


@pytest.fixture
def sample_detailed_products(db, sample_product, sample_colors, sample_sizes):
    """테스트용 상세 상품들"""
    from apps.products.models import DetailedProduct

    return [
        DetailedProduct.objects.create(
            product=sample_product, color=sample_colors[0], size=sample_sizes[0], stock=50
        ),
        DetailedProduct.objects.create(
            product=sample_product, color=sample_colors[0], size=sample_sizes[1], stock=30
        ),
    ]


@pytest.fixture
def sample_product_with_full_options(db, sample_menu, sample_category, sample_colors, sample_sizes):
    """색상/사이즈/이미지가 있는 상품"""
    from apps.products.models import DetailedProduct, Image, Product

    product = Product.objects.create(
        menu=sample_menu,
        category=sample_category,
        name="풀옵션 상품",
        price=25000,
        description="모든 옵션이 있는 상품",
    )

    # 이미지 추가
    Image.objects.create(
        product=product, image_url="https://example.com/full_thumb.jpg", is_thumbnail=True
    )

    # 상세 상품 추가
    DetailedProduct.objects.create(
        product=product, color=sample_colors[0], size=sample_sizes[0], stock=100
    )

    return product


@pytest.fixture
def sample_product_with_postings(db, sample_menu, sample_category, regular_user):
    """후기가 있는 상품"""
    from apps.postings.models import Posting
    from apps.products.models import Product

    product = Product.objects.create(
        menu=sample_menu,
        category=sample_category,
        name="후기있는 상품",
        price=20000,
        description="후기가 달린 상품",
    )

    # 후기 추가
    Posting.objects.create(
        product=product, user=regular_user, title="좋은 상품", content="정말 좋아요", rating=5
    )
    Posting.objects.create(
        product=product, user=regular_user, title="괜찮은 상품", content="나쁘지 않아요", rating=4
    )

    return product


@pytest.fixture
def get_product_detail_with_options(api_client, db):
    """상품 상세 조회 헬퍼 (확장 정보 포함)"""

    def _get_product_detail(product_id):
        url = API_PRODUCT_DETAIL.format(product_id=product_id)
        return api_client.get(url)

    return _get_product_detail


@pytest.fixture
def sample_products_with_thumbnails(db, sample_menu, sample_category):
    """썸네일이 있는 상품들"""
    from apps.products.models import Image, Product

    products = []
    for i in range(3):
        product = Product.objects.create(
            menu=sample_menu,
            category=sample_category,
            name=f"썸네일 상품 {i + 1}",
            price=10000 + (i * 1000),
            description=f"설명 {i + 1}",
        )
        Image.objects.create(
            product=product, image_url=f"https://example.com/thumb_{i + 1}.jpg", is_thumbnail=True
        )
        products.append(product)

    return products


@pytest.fixture
def get_products_with_thumbnails(api_client, db):
    """상품 목록 조회 헬퍼 (썸네일 포함)"""

    def _get_products():
        return api_client.get(API_PRODUCTS)

    return _get_products
