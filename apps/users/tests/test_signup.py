"""
회원가입 테스트
"""
import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_사용자는_필수정보를_입력하면_회원가입할_수_있다(signup, valid_signup_payload):
    """
    Given: 이메일, 비밀번호, 이름을 포함한 회원가입 정보
    When: 회원가입 요청을 보내면
    Then: 새로운 사용자가 생성된다
    """
    # When
    response = signup(valid_signup_payload)
    
    # Then
    assert response.status_code == 201
    assert get_user_model().objects.filter(email=valid_signup_payload["email"]).exists()
