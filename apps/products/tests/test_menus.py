"""
메뉴 테스트
"""


def test_사용자는_메뉴_목록을_조회할_수_있다(get_menus):
    """
    Given: 메뉴가 등록되어 있을 때
    When: 메뉴 목록을 조회하면
    Then: 메뉴 목록을 확인할 수 있다
    """
    # When
    response = get_menus()
    
    # Then
    assert response.status_code == 200
    assert isinstance(response.data, list)
