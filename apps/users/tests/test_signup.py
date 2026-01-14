"""
회원가입 테스트
"""


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
    assert response.data["email"] == valid_signup_payload["email"]
    assert response.data["name"] == valid_signup_payload["name"]
    assert "password" not in response.data


def test_이미_가입된_이메일로는_회원가입할_수_없다(signup, valid_signup_payload):
    """
    Given: 이미 가입된 이메일이 존재하고
    When: 동일한 이메일로 다시 회원가입을 시도하면
    Then: 회원가입이 실패한다
    """
    # Given: 첫 번째 회원가입 (성공)
    first_response = signup(valid_signup_payload)
    assert first_response.status_code == 201
    
    # When: 동일한 이메일로 다시 회원가입 시도
    second_response = signup(valid_signup_payload)
    
    # Then: 실패해야 함
    assert second_response.status_code == 400
    assert "email" in second_response.data


def test_이메일_형식이_아니면_회원가입할_수_없다(signup, valid_signup_payload):
    """
    Given: 잘못된 이메일 형식의 데이터
    When: 회원가입을 시도하면
    Then: 회원가입이 실패한다
    """
    # Given
    invalid_payload = valid_signup_payload.copy()
    invalid_payload["email"] = "notanemail"
    
    # When
    response = signup(invalid_payload)
    
    # Then
    assert response.status_code == 400
    assert "email" in response.data


def test_비밀번호_규칙을_만족하지_않으면_회원가입할_수_없다(signup, valid_signup_payload):
    """
    Given: 약한 비밀번호 (예: 짧거나 단순한 비밀번호)
    When: 회원가입을 시도하면
    Then: 회원가입이 실패한다
    """
    # Given: 너무 짧은 비밀번호
    weak_payload = valid_signup_payload.copy()
    weak_payload["password"] = "123"
    
    # When
    response = signup(weak_payload)
    
    # Then
    assert response.status_code == 400
    assert "password" in response.data
