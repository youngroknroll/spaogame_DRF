"""
로그인 테스트
"""


def test_사용자는_올바른_이메일과_비밀번호로_로그인할_수_있다(login, registered_user):
    """
    Given: 가입된 사용자의 이메일과 비밀번호
    When: 로그인을 시도하면
    Then: 로그인에 성공한다
    """
    # Given
    credentials = {
        "email": registered_user["email"],
        "password": registered_user["password"],
    }
    
    # When
    response = login(credentials)
    
    # Then
    assert response.status_code == 200
