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


def test_관리자_관리자는_카테고리를_등록할_수_있다(create_category, sample_menu):
    """
    Given: 관리자 권한과 메뉴가 있을 때
    When: 카테고리를 등록하면
    Then: 카테고리가 생성된다
    """
    # Given
    payload = {
        "menu": sample_menu.id,
        "name": "후라이드",
    }
    
    # When
    response = create_category(sample_menu.id, payload)
    
    # Then
    assert response.status_code == 201
    assert response.data["name"] == "후라이드"
    assert response.data["menu"] == sample_menu.id
    assert "id" in response.data
