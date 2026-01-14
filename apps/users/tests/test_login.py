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


def test_로그인에_성공하면_인증_토큰을_발급받는다(login, registered_user):
    """
    Given: 가입된 사용자의 이메일과 비밀번호
    When: 로그인을 하면
    Then: access 토큰과 refresh 토큰을 발급받는다
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
    assert "access" in response.data
    assert "refresh" in response.data
    assert len(response.data["access"]) > 0
    assert len(response.data["refresh"]) > 0


def test_비밀번호가_틀리면_로그인할_수_없다(login, registered_user):
    """
    Given: 가입된 사용자의 이메일과 잘못된 비밀번호
    When: 로그인을 시도하면
    Then: 로그인이 실패한다
    """
    # Given
    credentials = {
        "email": registered_user["email"],
        "password": "WrongPassword123!",
    }
    
    # When
    response = login(credentials)
    
    # Then
    assert response.status_code == 401


def test_존재하지_않는_이메일로는_로그인할_수_없다(login):
    """
    Given: 존재하지 않는 이메일
    When: 로그인을 시도하면
    Then: 로그인이 실패한다
    """
    # Given
    credentials = {
        "email": "notexist@example.com",
        "password": "SomePassword123!",
    }
    
    # When
    response = login(credentials)
    
    # Then
    assert response.status_code == 401
