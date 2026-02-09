"""
후기 CRUD 테스트 (목록, 상세, 수정, 삭제)
"""

import pytest
from rest_framework import status

from apps.postings.models import Posting

# API URLs
API_POSTINGS_LIST_ALL = "/api/postings/"
API_POSTING_DETAIL = "/api/postings/{posting_id}/"


@pytest.fixture
def sample_posting(db, regular_user, sample_product):
    """테스트용 후기"""
    return Posting.objects.create(
        user=regular_user,
        product=sample_product,
        title="테스트 후기",
        content="테스트 내용입니다.",
        rating=4,
    )


@pytest.fixture
def another_user_posting(db, sample_product):
    """다른 사용자의 후기"""
    from django.contrib.auth import get_user_model

    User = get_user_model()

    other_user = User.objects.create_user(
        email="other@example.com", password="OtherPass123!", name="다른사용자"
    )

    return Posting.objects.create(
        user=other_user,
        product=sample_product,
        title="다른 사용자 후기",
        content="다른 사용자 내용입니다.",
        rating=3,
    )


# ============================================================
# 후기 목록 조회 테스트
# ============================================================


def test_사용자는_후기_목록을_조회할_수_있다(api_client, sample_posting, another_user_posting):
    """
    Given: 여러 후기가 존재할 때
    When: 후기 목록을 조회하면
    Then: 모든 후기가 조회된다
    """
    response = api_client.get(API_POSTINGS_LIST_ALL)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data["results"]) >= 2  # 최소 2개 이상


# ============================================================
# 후기 상세 조회 테스트
# ============================================================


def test_사용자는_특정_후기의_상세_정보를_조회할_수_있다(api_client, sample_posting):
    """
    Given: 후기가 존재할 때
    When: 특정 후기의 상세 정보를 조회하면
    Then: 후기의 상세 정보가 반환된다
    """
    url = API_POSTING_DETAIL.format(posting_id=sample_posting.id)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["id"] == sample_posting.id
    assert response.data["title"] == "테스트 후기"
    assert response.data["content"] == "테스트 내용입니다."
    assert response.data["rating"] == 4


# ============================================================
# 후기 수정 테스트
# ============================================================


@pytest.mark.django_db
def test_인증_후기_작성자는_자신의_후기를_수정할_수_있다(user_client, sample_posting):
    """
    Given: 로그인한 사용자가 작성한 후기가 있을 때
    When: 자신의 후기를 수정하면
    Then: 후기가 수정된다
    """
    url = API_POSTING_DETAIL.format(posting_id=sample_posting.id)
    update_data = {"title": "수정된 제목", "content": "수정된 내용", "rating": 5}

    response = user_client.patch(url, update_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "수정된 제목"
    assert response.data["content"] == "수정된 내용"
    assert response.data["rating"] == 5


@pytest.mark.django_db
def test_권한_후기_작성자가_아닌_사용자는_후기를_수정할_수_없다(user_client, another_user_posting):
    """
    Given: 다른 사용자가 작성한 후기가 있을 때
    When: 로그인한 사용자가 다른 사용자의 후기를 수정하려고 하면
    Then: 권한 오류가 발생한다
    """
    url = API_POSTING_DETAIL.format(posting_id=another_user_posting.id)
    update_data = {"title": "수정 시도", "content": "수정 시도", "rating": 1}

    response = user_client.patch(url, update_data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


# ============================================================
# 후기 삭제 테스트
# ============================================================


@pytest.mark.django_db
def test_인증_후기_작성자는_자신의_후기를_삭제할_수_있다(user_client, sample_posting):
    """
    Given: 로그인한 사용자가 작성한 후기가 있을 때
    When: 자신의 후기를 삭제하면
    Then: 후기가 삭제된다
    """
    url = API_POSTING_DETAIL.format(posting_id=sample_posting.id)

    response = user_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Posting.objects.filter(id=sample_posting.id).exists()


@pytest.mark.django_db
def test_권한_후기_작성자가_아닌_사용자는_후기를_삭제할_수_없다(user_client, another_user_posting):
    """
    Given: 다른 사용자가 작성한 후기가 있을 때
    When: 로그인한 사용자가 다른 사용자의 후기를 삭제하려고 하면
    Then: 권한 오류가 발생한다
    """
    url = API_POSTING_DETAIL.format(posting_id=another_user_posting.id)

    response = user_client.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert Posting.objects.filter(id=another_user_posting.id).exists()


# ============================================================
# 존재하지 않는 후기 테스트
# ============================================================


def test_존재하지_않는_후기는_조회_수정_삭제할_수_없다(user_client):
    """
    Given: 존재하지 않는 후기 ID로
    When: 조회/수정/삭제를 시도하면
    Then: 404 오류가 발생한다
    """
    non_existent_id = 99999
    url = API_POSTING_DETAIL.format(posting_id=non_existent_id)

    # 조회
    response = user_client.get(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # 수정
    response = user_client.patch(url, {"title": "수정"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # 삭제
    response = user_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
