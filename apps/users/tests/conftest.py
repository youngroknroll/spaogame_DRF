"""
Users 앱 테스트 픽스처
"""

import pytest

from apps.conftest import (
    API_USERS_GENDERS,
    API_USERS_LOGIN,
    API_USERS_SIGNUP,
    TEST_USER_EMAIL,
    TEST_USER_NAME,
    TEST_USER_PASSWORD,
)


@pytest.fixture
def valid_signup_payload():
    """유효한 회원가입 데이터 (기본)"""
    return {
        "email": TEST_USER_EMAIL,
        "password": TEST_USER_PASSWORD,
        "name": TEST_USER_NAME,
    }


@pytest.fixture
def full_signup_payload():
    """유효한 회원가입 데이터 (전체 필드)"""
    return {
        "email": "fulluser@example.com",
        "password": TEST_USER_PASSWORD,
        "name": "풀유저",
        "username": "fulluser",
        "mobile_number": "010-1234-5678",
        "address1": "서울시 강남구 테헤란로 123",
        "address2": "스파오빌딩 5층",
        "birthday": "1990-01-15",
        "gender": "M",
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


@pytest.fixture
def get_genders(api_client):
    """성별 목록 조회 헬퍼"""

    def _get_genders():
        return api_client.get(API_USERS_GENDERS)

    return _get_genders
