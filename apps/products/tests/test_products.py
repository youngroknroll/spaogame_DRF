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


def test_권한_관리자가_아닌_사용자는_상품을_등록할_수_없다(create_product_as_user, sample_menu, sample_category):
    """
    Given: 일반 사용자 권한이고, 메뉴와 카테고리가 존재할 때
    When: 상품을 등록하려고 하면
    Then: 권한 오류가 발생한다
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
    response = create_product_as_user(payload)
    
    # Then
    assert response.status_code == 403


def test_사용자는_특정_메뉴와_카테고리에_속한_상품_목록을_조회할_수_있다(get_products, sample_products):
    """
    Given: 특정 메뉴와 카테고리에 상품들이 등록되어 있을 때
    When: 해당 메뉴와 카테고리로 상품 목록을 조회하면
    Then: 상품 목록이 반환된다
    """
    # Given
    menu_id = sample_products[0].menu.id
    category_id = sample_products[0].category.id
    
    # When
    response = get_products(menu_id=menu_id, category_id=category_id)
    
    # Then
    assert response.status_code == 200
    assert len(response.data["results"]) == 2
    assert response.data["results"][0]["name"] == "후라이드치킨"
    assert response.data["results"][1]["name"] == "양념치킨"


def test_검증_카테고리가_메뉴에_속하지_않으면_상품을_등록할_수_없다(create_product, sample_menu, db):
    """
    Given: 메뉴와 다른 메뉴에 속한 카테고리가 있을 때
    When: 해당 카테고리로 상품을 등록하려고 하면
    Then: 검증 오류가 발생한다
    """
    # Given - 다른 메뉴 생성
    from apps.products.models import Menu, Category
    other_menu = Menu.objects.create(name="피자")
    other_category = Category.objects.create(menu=other_menu, name="치즈피자")
    
    payload = {
        "menu": sample_menu.id,
        "category": other_category.id,  # 다른 메뉴의 카테고리
        "name": "후라이드치킨",
        "price": 18000,
        "description": "바삭한 후라이드치킨",
    }
    
    # When
    response = create_product(payload)
    
    # Then
    assert response.status_code == 400
    assert "category" in response.data or "non_field_errors" in response.data


def test_사용자는_상품_상세_정보를_조회할_수_있다(get_product_detail, sample_products):
    """
    Given: 상품이 등록되어 있을 때
    When: 상품 ID로 상세 정보를 조회하면
    Then: 상품 상세 정보가 반환된다
    """
    # Given
    product = sample_products[0]
    
    # When
    response = get_product_detail(product.id)
    
    # Then
    assert response.status_code == 200
    assert response.data["id"] == product.id
    assert response.data["name"] == "후라이드치킨"
    assert response.data["price"] == 18000