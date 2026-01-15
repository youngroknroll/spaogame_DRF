"""
상품 테스트
"""


def test_관리자_관리자는_상품을_등록할_수_있다(create_product, sample_menu, sample_category):
    """
    Given: 관리자 권한이 있고, 메뉴와 카테고리가 존재할 때
    When: 상품을 등록하면
    Then: 상품이 생성된다
    """
    # Given
    payload = {
        "menu": sample_menu.id,
        "category": sample_category.id,
        "name": "후라이드치킨",
        "price": 18000,
        "description": "바삭한 후라이드치킨",
    }
    
    # When
    response = create_product(payload)
    
    # Then
    assert response.status_code == 201
    assert response.data["name"] == "후라이드치킨"
    assert response.data["price"] == 18000
    assert "id" in response.data
