"""
전체 프로젝트 공통 테스트 설정
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

# ============================================================
# 테스트 상수 (한 곳에서 관리)
# ============================================================

# API URL
API_USERS_SIGNUP = "/api/users/signup/"
API_USERS_LOGIN = "/api/users/login/"
API_PRODUCTS_MENUS = "/api/products/menus/"
API_PRODUCTS_CATEGORIES = "/api/products/menus/{menu_id}/categories/"
API_PRODUCTS = "/api/products/"
API_PRODUCT_DETAIL = "/api/products/{product_id}/"

# 관리자 계정 정보
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "AdminPass123!"
ADMIN_NAME = "관리자"

# 일반 사용자 테스트 데이터
TEST_USER_EMAIL = "user@example.com"
TEST_USER_PASSWORD = "StrongPass123!"
TEST_USER_NAME = "테스트유저"


# ============================================================
# 공통 Fixture
# ============================================================

@pytest.fixture
def api_client():
    """API 클라이언트"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """관리자 사용자 (DB에 저장)"""
    return User.objects.create_user(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        name=ADMIN_NAME,
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin_token(api_client, admin_user):
    """관리자 인증 토큰"""
    response = api_client.post(API_USERS_LOGIN, {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
    })
    return response.data["access"]


@pytest.fixture
def auth_client(api_client, admin_token):
    """인증된 API 클라이언트 (관리자)"""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    return api_client


@pytest.fixture
def regular_user(db):
    """일반 사용자 (DB에 저장)"""
    return User.objects.create_user(
        email=TEST_USER_EMAIL,
        password=TEST_USER_PASSWORD,
        name=TEST_USER_NAME,
    )


@pytest.fixture
def regular_user_token(api_client, regular_user):
    """일반 사용자 인증 토큰"""
    response = api_client.post(API_USERS_LOGIN, {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
    })
    return response.data["access"]


@pytest.fixture
def user_client(api_client, regular_user_token):
    """인증된 API 클라이언트 (일반 사용자)"""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {regular_user_token}")
    return client
