"""
Users 프로필 조회/수정 테스트
"""
import pytest
from rest_framework import status
from apps.conftest import TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_USER_NAME


API_USERS_PROFILE = "/api/users/profile/"


@pytest.fixture
def get_profile(api_client):
    """프로필 조회 헬퍼"""
    def _get_profile():
        return api_client.get(API_USERS_PROFILE)
    return _get_profile


@pytest.fixture
def update_profile(api_client):
    """프로필 수정 헬퍼"""
    def _update_profile(payload):
        return api_client.patch(API_USERS_PROFILE, payload)
    return _update_profile


# ============================================================
# 프로필 조회 테스트
# ============================================================


@pytest.mark.django_db
def test_인증_로그인한_사용자는_자신의_프로필을_조회할_수_있다(user_client, regular_user):
    """로그인한 사용자는 자신의 프로필을 조회할 수 있다"""
    response = user_client.get(API_USERS_PROFILE)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == TEST_USER_EMAIL
    assert response.data["name"] == TEST_USER_NAME
    assert "password" not in response.data  # 비밀번호는 응답에 포함되지 않음


def test_인증_비로그인_사용자는_프로필을_조회할_수_없다(api_client):
    """비로그인 사용자는 프로필을 조회할 수 없다"""
    response = api_client.get(API_USERS_PROFILE)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ============================================================
# 프로필 수정 테스트
# ============================================================


@pytest.mark.django_db
def test_인증_로그인한_사용자는_자신의_프로필을_수정할_수_있다(user_client, regular_user):
    """로그인한 사용자는 자신의 프로필을 수정할 수 있다"""
    update_data = {
        "name": "수정된이름",
        "username": "updated_user",
        "mobile_number": "010-9999-8888",
        "address1": "서울시 강남구",
    }

    response = user_client.patch(API_USERS_PROFILE, update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "수정된이름"
    assert response.data["username"] == "updated_user"
    assert response.data["mobile_number"] == "010-9999-8888"
    assert response.data["address1"] == "서울시 강남구"


@pytest.mark.django_db
def test_검증_프로필_수정시_이메일은_변경할_수_없다(user_client, regular_user):
    """프로필 수정 시 이메일은 변경할 수 없다"""
    update_data = {
        "email": "newemail@example.com",
        "name": "수정된이름",
    }

    response = user_client.patch(API_USERS_PROFILE, update_data)

    # 이메일은 read_only이므로 무시되어야 함
    assert response.status_code == status.HTTP_200_OK
    assert response.data["email"] == TEST_USER_EMAIL  # 기존 이메일 유지


@pytest.mark.django_db
def test_검증_프로필_수정시_전화번호_형식이_잘못되면_실패한다(user_client, regular_user):
    """프로필 수정 시 전화번호 형식이 잘못되면 실패한다"""
    update_data = {
        "mobile_number": "01012345678",  # 하이픈 없음
    }

    response = user_client.patch(API_USERS_PROFILE, update_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "mobile_number" in response.data
