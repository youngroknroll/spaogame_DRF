"""
Users 앱 테스트 픽스처
"""
import pytest
from apps.conftest import (
    API_USERS_SIGNUP,
    API_USERS_LOGIN,
    TEST_USER_EMAIL,
    TEST_USER_PASSWORD,
    TEST_USER_NAME,
)


@pytest.fixture
def valid_signup_payload():
    """유효한 회원가입 데이터"""
    return {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "name": TEST_USER_NAME,
    }


@pytest.fixture
def signup(api_client, db):
    """회원가입 요청 헬퍼 (DB 접근 필요)"""
    def _signup(payload):
        return api_client.post(API_USERS_SIGNUP, payload)
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
        return api_client.post(API_USERS_LOGIN, credentials)
    return _login
