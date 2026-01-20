"""
성별 목록 테스트
"""


def test_사용자는_성별_목록을_조회할_수_있다(get_genders):
    """
    Given: 성별 선택지가 정의되어 있을 때
    When: 성별 목록을 조회하면
    Then: 성별 목록이 반환된다
    """
    # When
    response = get_genders()

    # Then
    assert response.status_code == 200
    assert response.data == [
        {"value": "M", "label": "남성"},
        {"value": "F", "label": "여성"},
    ]
