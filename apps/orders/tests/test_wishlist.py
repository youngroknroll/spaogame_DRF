"""
위시리스트 테스트
"""


def test_인증_로그인한_사용자는_위시리스트에_상품을_추가할_수_있다(add_to_wishlist, sample_product):
    """
    Given: 로그인한 사용자와 상품이 있을 때
    When: 위시리스트에 상품을 추가하면
    Then: 위시리스트에 상품이 추가된다
    """
    # Given
    payload = {
        "product_id": sample_product.id
    }

    # When
    response = add_to_wishlist(payload)

    # Then
    assert response.status_code == 201
    assert response.data["product"]["id"] == sample_product.id


def test_정책_같은_상품을_중복_추가해도_항목은_하나만_유지된다(
    add_to_wishlist, get_wishlist, sample_product
):
    """
    Given: 위시리스트에 동일한 상품을 추가할 때
    When: 같은 상품을 두 번 추가하면
    Then: 항목은 하나만 유지되고 두 번째 추가는 200을 반환한다
    """
    # Given
    add_to_wishlist({"product_id": sample_product.id})

    # When
    second_response = add_to_wishlist({"product_id": sample_product.id})
    list_response = get_wishlist()

    # Then
    assert second_response.status_code == 200
    assert len(list_response.data["items"]) == 1


def test_인증_로그인한_사용자는_위시리스트를_조회할_수_있다(
    add_to_wishlist, get_wishlist, sample_product
):
    """
    Given: 위시리스트에 상품이 담겨 있을 때
    When: 위시리스트를 조회하면
    Then: 위시리스트 목록이 반환된다
    """
    # Given
    add_to_wishlist({"product_id": sample_product.id})

    # When
    response = get_wishlist()

    # Then
    assert response.status_code == 200
    assert len(response.data["items"]) >= 1


def test_인증_로그인한_사용자는_위시리스트에서_상품을_삭제할_수_있다(
    add_to_wishlist, remove_from_wishlist, get_wishlist, sample_product
):
    """
    Given: 위시리스트에 상품이 담겨 있을 때
    When: 위시리스트에서 상품을 삭제하면
    Then: 위시리스트에서 삭제된다
    """
    # Given
    add_response = add_to_wishlist({"product_id": sample_product.id})
    item_id = add_response.data["id"]

    # When
    response = remove_from_wishlist(item_id)

    # Then
    assert response.status_code == 204

    # 위시리스트 조회 시 비어있어야 함
    wishlist_response = get_wishlist()
    assert wishlist_response.data["items"] == []


def test_비인증_사용자는_위시리스트를_조회할_수_없다(get_wishlist_anonymous):
    """
    Given: 로그인하지 않은 사용자
    When: 위시리스트를 조회하면
    Then: 인증 오류가 발생한다
    """
    # When
    response = get_wishlist_anonymous()

    # Then
    assert response.status_code == 401


def test_비인증_사용자는_위시리스트에_상품을_추가할_수_없다(
    add_to_wishlist_anonymous, sample_product
):
    """
    Given: 로그인하지 않은 사용자와 상품이 있을 때
    When: 위시리스트에 상품을 추가하면
    Then: 인증 오류가 발생한다
    """
    # When
    response = add_to_wishlist_anonymous({"product_id": sample_product.id})

    # Then
    assert response.status_code == 401


def test_비인증_사용자는_위시리스트에서_상품을_삭제할_수_없다(
    remove_from_wishlist_anonymous, wishlist_item
):
    """
    Given: 로그인하지 않은 사용자와 위시리스트 항목이 있을 때
    When: 위시리스트 항목을 삭제하면
    Then: 인증 오류가 발생한다
    """
    # When
    response = remove_from_wishlist_anonymous(wishlist_item.id)

    # Then
    assert response.status_code == 401
