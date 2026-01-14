"""
Products 테스트 픽스처
"""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """API 클라이언트"""
    return APIClient()


@pytest.fixture
def get_menus(api_client, db):
    """메뉴 목록 조회 헬퍼 (DB 접근 필요)"""
    def _get_menus():
        return api_client.get("/api/products/menus/")
    return _get_menus
