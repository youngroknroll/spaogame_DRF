"""
회원가입 테스트
"""
from django.contrib.auth import get_user_model

User = get_user_model()


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


def test_회원가입시_비밀번호는_평문으로_저장되지_않는다(signup, valid_signup_payload):
    """
    Given: 유효한 회원가입 정보
    When: 회원가입을 하면
    Then: 비밀번호가 해시되어 저장되고 실제로 작동한다
    """
    # Given
    plain_password = valid_signup_payload["password"]
    
    # When
    response = signup(valid_signup_payload)
    assert response.status_code == 201
    
    # Then: DB에서 사용자를 조회하고 비밀번호 검증
    user = User.objects.get(email=valid_signup_payload["email"])
    
    # 평문으로 저장되지 않았는지 확인
    assert user.password != plain_password
    
    # 해시 형식 확인 (Argon2 사용)
    assert user.password.startswith("argon2")
    
    # 실제로 비밀번호가 작동하는지 확인
    assert user.check_password(plain_password) is True
    assert user.check_password("wrongpassword") is False


# ============================================================
# P1: 확장 필드 테스트
# ============================================================

def test_회원가입시_전체필드를_저장할_수_있다(signup, full_signup_payload):
    """
    Given: 전체 필드가 포함된 회원가입 정보
    When: 회원가입을 하면
    Then: 모든 필드가 저장된다
    """
    # When
    response = signup(full_signup_payload)
    
    # Then
    assert response.status_code == 201
    assert response.data["email"] == full_signup_payload["email"]
    assert response.data["name"] == full_signup_payload["name"]
    assert response.data["username"] == full_signup_payload["username"]
    assert response.data["mobile_number"] == full_signup_payload["mobile_number"]
    assert response.data["address1"] == full_signup_payload["address1"]
    assert response.data["address2"] == full_signup_payload["address2"]
    assert response.data["birthday"] == full_signup_payload["birthday"]
    assert response.data["gender"] == full_signup_payload["gender"]
    
    # DB 저장 확인
    user = User.objects.get(email=full_signup_payload["email"])
    assert user.username == full_signup_payload["username"]
    assert user.mobile_number == full_signup_payload["mobile_number"]


def test_회원가입시_전화번호_형식이_잘못되면_실패한다(signup, full_signup_payload):
    """
    Given: 잘못된 전화번호 형식의 데이터
    When: 회원가입을 시도하면
    Then: 회원가입이 실패한다
    """
    # Given
    invalid_payload = full_signup_payload.copy()
    invalid_payload["mobile_number"] = "12345"  # 잘못된 형식
    
    # When
    response = signup(invalid_payload)
    
    # Then
    assert response.status_code == 400
    assert "mobile_number" in response.data


def test_회원가입시_성별은_M_F_중_하나여야_한다(signup, full_signup_payload):
    """
    Given: 잘못된 성별 값의 데이터
    When: 회원가입을 시도하면
    Then: 회원가입이 실패한다
    """
    # Given
    invalid_payload = full_signup_payload.copy()
    invalid_payload["gender"] = "X"  # 잘못된 값
    
    # When
    response = signup(invalid_payload)
    
    # Then
    assert response.status_code == 400
    assert "gender" in response.data
