"""
Postings 앱 테스트 픽스처
- 공통 픽스처는 apps/conftest.py 사용
- 이 파일에는 Postings 앱 전용 픽스처만 정의
"""
import pytest
from apps.conftest import API_POSTINGS, API_COMMENTS, API_COMMENT


@pytest.fixture
def create_posting(user_client, db):
    """후기 작성 헬퍼 (인증된 사용자)"""
    def _create_posting(product_id, payload):
        url = API_POSTINGS.format(product_id=product_id)
        return user_client.post(url, payload)
    return _create_posting


@pytest.fixture
def create_posting_anonymous(api_client, db):
    """후기 작성 헬퍼 (비인증 사용자)"""
    def _create_posting(product_id, payload):
        url = API_POSTINGS.format(product_id=product_id)
        return api_client.post(url, payload)
    return _create_posting


@pytest.fixture
def create_comment(user_client, db):
    """댓글 작성 헬퍼 (인증된 사용자)"""
    def _create_comment(posting_id, payload):
        url = API_COMMENTS.format(posting_id=posting_id)
        return user_client.post(url, payload)
    return _create_comment


@pytest.fixture
def delete_comment(user_client, db):
    """댓글 삭제 헬퍼 (인증된 사용자)"""
    def _delete_comment(posting_id, comment_id):
        url = API_COMMENT.format(posting_id=posting_id, comment_id=comment_id)
        return user_client.delete(url)
    return _delete_comment
