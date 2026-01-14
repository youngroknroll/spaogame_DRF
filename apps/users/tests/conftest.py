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
    """유효한 회원가입 데이터 (매번 새로운 복사본 반환)"""
    def _payload():
        return {
            "email": "user@example.com",
            "password": "StrongPass123!",
            "name": "테스트유저",
        }
    return _payload()


@pytest.fixture
def signup(api_client, db):
    """회원가입 요청 헬퍼 (DB 접근 필요)"""
    def _signup(payload):
        return api_client.post("/api/users/signup/", payload)
    return _signup


@pytest.fixture
def registered_user(signup, valid_signup_payload):
    """가입된 사용자 (비밀번호 포함)"""
    signup(valid_signup_payload)
    return valid_signup_payload


@pytest.fixture
def login(api_client, db):
    """로그인 요청 헬퍼 (DB 접근 필요)"""
    def _login(credentials):
        return api_client.post("/api/users/login/", credentials)
    return _login
