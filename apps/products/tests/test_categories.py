"""
카테고리 테스트
"""


def test_사용자는_특정_메뉴에_속한_카테고리_목록을_조회할_수_있다(get_categories, sample_menu):
    """
    Given: 특정 메뉴에 카테고리가 등록되어 있을 때
    When: 해당 메뉴의 카테고리 목록을 조회하면
    Then: 카테고리 목록을 확인할 수 있다
    """
    # When
    response = get_categories(sample_menu.id)
    
    # Then
    assert response.status_code == 200
    assert isinstance(response.data, list)
