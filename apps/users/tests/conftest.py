"""
테스트 픽스처
"""
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """API 클라이언트"""
    return APIClient()


@pytest.fixture
def valid_signup_payload():
    """유효한 회원가입 데이터"""
    return {
        "email": "user@example.com",
        "password": "StrongPass123!",
        "name": "테스트유저",
    }


@pytest.fixture
def signup(api_client, db):
    """회원가입 요청 헬퍼 (DB 접근 필요)"""
    def _signup(payload):
        return api_client.post("/api/users/signup/", payload)
    return _signup
