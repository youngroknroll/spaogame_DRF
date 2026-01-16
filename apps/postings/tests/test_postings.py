"""
후기 테스트
"""


def test_인증_로그인한_사용자는_상품에_대한_후기를_작성할_수_있다(create_posting, sample_product):
    """
    Given: 로그인한 사용자와 상품이 있을 때
    When: 후기를 작성하면
    Then: 후기가 생성된다
    """
    # Given
    payload = {
        "title": "맛있어요!",
        "content": "정말 맛있게 잘 먹었습니다.",
        "rating": 5
    }
    
    # When
    response = create_posting(sample_product.id, payload)
    
    # Then
    assert response.status_code == 201
    assert response.data["title"] == "맛있어요!"
    assert response.data["content"] == "정말 맛있게 잘 먹었습니다."
    assert response.data["rating"] == 5


def test_인증_로그인하지_않은_사용자는_후기를_작성할_수_없다(create_posting_anonymous, sample_product):
    """
    Given: 비로그인 상태에서
    When: 후기를 작성하려고 하면
    Then: 인증 오류가 발생한다
    """
    # Given
    payload = {
        "title": "맛있어요!",
        "content": "정말 맛있게 잘 먹었습니다.",
        "rating": 5
    }
    
    # When
    response = create_posting_anonymous(sample_product.id, payload)
    
    # Then
    assert response.status_code == 401
