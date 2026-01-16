"""
장바구니 테스트
"""


def test_인증_로그인한_사용자는_상품을_장바구니에_담을_수_있다(add_to_cart, sample_product):
    """
    Given: 로그인한 사용자와 상품이 있을 때
    When: 상품을 장바구니에 담으면
    Then: 장바구니에 상품이 추가된다
    """
    # Given
    payload = {
        "product_id": sample_product.id,
        "quantity": 2
    }
    
    # When
    response = add_to_cart(payload)
    
    # Then
    assert response.status_code == 201
    assert response.data["product"]["id"] == sample_product.id
    assert response.data["quantity"] == 2


def test_인증_로그인한_사용자는_자신의_장바구니를_조회할_수_있다(get_cart):
    """
    Given: 로그인한 사용자가 있을 때
    When: 장바구니를 조회하면
    Then: 장바구니 정보가 반환된다
    """
    # When
    response = get_cart()
    
    # Then
    assert response.status_code == 200
    assert "items" in response.data


def test_인증_장바구니가_비어_있어도_정상적으로_조회된다(get_cart):
    """
    Given: 로그인한 사용자에게 장바구니가 없을 때
    When: 장바구니를 조회하면
    Then: 빈 장바구니가 반환된다
    """
    # When
    response = get_cart()
    
    # Then
    assert response.status_code == 200
    assert response.data["items"] == []


def test_인증_로그인한_사용자는_장바구니_상품의_수량을_변경할_수_있다(
    add_to_cart, update_cart_item, sample_product
):
    """
    Given: 장바구니에 상품이 담겨 있을 때
    When: 상품 수량을 변경하면
    Then: 수량이 업데이트된다
    """
    # Given - 상품을 장바구니에 담기
    add_response = add_to_cart({"product_id": sample_product.id, "quantity": 2})
    item_id = add_response.data["id"]
    
    # When - 수량 변경
    response = update_cart_item(item_id, {"quantity": 5})
    
    # Then
    assert response.status_code == 200
    assert response.data["quantity"] == 5


def test_인증_로그인한_사용자는_장바구니에서_상품을_제거할_수_있다(
    add_to_cart, remove_from_cart, get_cart, sample_product
):
    """
    Given: 장바구니에 상품이 담겨 있을 때
    When: 상품을 제거하면
    Then: 장바구니에서 삭제된다
    """
    # Given - 상품을 장바구니에 담기
    add_response = add_to_cart({"product_id": sample_product.id, "quantity": 2})
    item_id = add_response.data["id"]
    
    # When - 상품 제거
    response = remove_from_cart(item_id)
    
    # Then
    assert response.status_code == 204
    
    # 장바구니 조회 시 비어있어야 함
    cart_response = get_cart()
    assert cart_response.data["items"] == []


def test_권한_다른_사용자의_장바구니는_수정하거나_삭제할_수_없다(
    add_to_cart, sample_product, api_client, db
):
    """
    Given: 다른 사용자의 장바구니 항목이 있을 때
    When: 다른 사용자가 해당 항목을 수정/삭제하려고 하면
    Then: 404 오류가 발생한다
    """
    from apps.conftest import (
        ADMIN_EMAIL, ADMIN_PASSWORD, API_USERS_LOGIN, API_CART_ITEM
    )
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Given - 첫 번째 사용자(regular_user)가 장바구니에 상품 추가
    add_response = add_to_cart({"product_id": sample_product.id, "quantity": 2})
    item_id = add_response.data["id"]
    
    # 두 번째 사용자(admin) 로그인
    admin_user = User.objects.create_user(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        name="관리자",
        is_staff=True,
    )
    login_response = api_client.post(API_USERS_LOGIN, {
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD,
    })
    admin_token = login_response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")
    
    # When - 다른 사용자의 장바구니 항목을 수정하려고 시도
    url = API_CART_ITEM.format(item_id=item_id)
    patch_response = api_client.patch(url, {"quantity": 10})
    
    # Then - 404 오류 발생
    assert patch_response.status_code == 404
    
    # When - 다른 사용자의 장바구니 항목을 삭제하려고 시도
    delete_response = api_client.delete(url)
    
    # Then - 404 오류 발생
    assert delete_response.status_code == 404
