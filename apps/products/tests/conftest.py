"""
Products 테스트 픽스처
"""
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    """API 클라이언트"""
    return APIClient()


@pytest.fixture
def admin_user(db):
    """관리자 사용자 (DB에 저장)"""
    return User.objects.create_user(
        email="admin@example.com",
        password="AdminPass123!",
        name="관리자",
        is_staff=True,
        is_superuser=True,
    )


@pytest.fixture
def admin_token(api_client, admin_user):
    """관리자 토큰"""
    response = api_client.post("/api/users/login/", {
        "email": admin_user.email,
        "password": "AdminPass123!",
    })
    return response.data["access"]


@pytest.fixture
def auth_client(api_client, admin_token):
    """인증된 API 클라이언트 (관리자)"""
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    return api_client


@pytest.fixture
def get_menus(api_client, db):
    """메뉴 목록 조회 헬퍼 (DB 접근 필요)"""
    def _get_menus():
        return api_client.get("/api/products/menus/")
    return _get_menus


@pytest.fixture
def create_menu(auth_client):
    """메뉴 등록 헬퍼 (관리자 인증)"""
    def _create_menu(payload):
        return auth_client.post("/api/products/menus/", payload)
    return _create_menu
