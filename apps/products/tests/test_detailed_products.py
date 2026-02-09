"""
상품 상세 도메인 테스트 (Color, Size, Image, DetailedProduct)
"""


# ============================================================
# Color 테스트
# ============================================================


def test_관리자는_색상을_등록할_수_있다(create_color):
    """
    Given: 관리자 권한이 있을 때
    When: 색상을 등록하면
    Then: 색상이 생성된다
    """
    # Given
    payload = {"name": "레드", "code": "#FF0000"}

    # When
    response = create_color(payload)

    # Then
    assert response.status_code == 201
    assert response.data["name"] == "레드"
    assert response.data["code"] == "#FF0000"


def test_사용자는_색상_목록을_조회할_수_있다(get_colors, sample_colors):
    """
    Given: 색상이 등록되어 있을 때
    When: 색상 목록을 조회하면
    Then: 색상 목록이 반환된다
    """
    # When
    response = get_colors()

    # Then
    assert response.status_code == 200
    assert len(response.data) >= 2


# ============================================================
# Size 테스트
# ============================================================


def test_관리자는_사이즈를_등록할_수_있다(create_size):
    """
    Given: 관리자 권한이 있을 때
    When: 사이즈를 등록하면
    Then: 사이즈가 생성된다
    """
    # Given
    payload = {"name": "M", "display_order": 2}

    # When
    response = create_size(payload)

    # Then
    assert response.status_code == 201
    assert response.data["name"] == "M"


def test_사용자는_사이즈_목록을_조회할_수_있다(get_sizes, sample_sizes):
    """
    Given: 사이즈가 등록되어 있을 때
    When: 사이즈 목록을 조회하면
    Then: 사이즈 목록이 반환된다
    """
    # When
    response = get_sizes()

    # Then
    assert response.status_code == 200
    assert len(response.data) >= 2


# ============================================================
# Image 테스트
# ============================================================


def test_관리자는_상품_이미지를_등록할_수_있다(create_image, sample_product):
    """
    Given: 관리자 권한과 상품이 있을 때
    When: 상품 이미지를 등록하면
    Then: 이미지가 생성된다
    """
    # Given
    payload = {
        "product": sample_product.id,
        "image_url": "https://example.com/image.jpg",
        "is_thumbnail": True,
    }

    # When
    response = create_image(payload)

    # Then
    assert response.status_code == 201
    assert response.data["image_url"] == "https://example.com/image.jpg"
    assert response.data["is_thumbnail"] is True


def test_사용자는_상품_이미지_목록을_조회할_수_있다(get_images, sample_images, sample_product):
    """
    Given: 상품에 이미지가 등록되어 있을 때
    When: 이미지 목록을 조회하면
    Then: 이미지 목록이 반환된다
    """
    # When
    response = get_images(sample_product.id)

    # Then
    assert response.status_code == 200
    assert len(response.data) >= 1


# ============================================================
# DetailedProduct 테스트
# ============================================================


def test_관리자는_상세상품을_등록할_수_있다(
    create_detailed_product, sample_product, sample_colors, sample_sizes
):
    """
    Given: 관리자 권한과 상품, 색상, 사이즈가 있을 때
    When: 상세 상품을 등록하면
    Then: 상세 상품이 생성된다
    """
    # Given
    payload = {
        "product": sample_product.id,
        "color": sample_colors[0].id,
        "size": sample_sizes[0].id,
        "stock": 100,
    }

    # When
    response = create_detailed_product(payload)

    # Then
    assert response.status_code == 201
    assert response.data["stock"] == 100


def test_사용자는_상세상품_목록을_조회할_수_있다(
    get_detailed_products, sample_detailed_products, sample_product
):
    """
    Given: 상품에 상세 상품이 등록되어 있을 때
    When: 상세 상품 목록을 조회하면
    Then: 상세 상품 목록이 반환된다
    """
    # When
    response = get_detailed_products(sample_product.id)

    # Then
    assert response.status_code == 200
    assert len(response.data) >= 1


def test_상품_상세에_색상_사이즈_이미지_정보가_포함된다(
    get_product_detail_with_options, sample_product_with_full_options
):
    """
    Given: 상품에 색상, 사이즈, 이미지가 등록되어 있을 때
    When: 상품 상세를 조회하면
    Then: 색상, 사이즈, 이미지 정보가 포함된다
    """
    # When
    response = get_product_detail_with_options(sample_product_with_full_options.id)

    # Then
    assert response.status_code == 200
    assert "colors" in response.data
    assert "sizes" in response.data
    assert "images" in response.data
    assert len(response.data["colors"]) >= 1
    assert len(response.data["sizes"]) >= 1
    assert len(response.data["images"]) >= 1


def test_상품_상세에_후기_댓글_집계_정보가_포함된다(
    get_product_detail_with_options, sample_product_with_postings
):
    """
    Given: 상품에 후기와 댓글이 등록되어 있을 때
    When: 상품 상세를 조회하면
    Then: 후기 개수와 평균 평점이 포함된다
    """
    # When
    response = get_product_detail_with_options(sample_product_with_postings.id)

    # Then
    assert response.status_code == 200
    assert "posting_count" in response.data
    assert "average_rating" in response.data
    assert response.data["posting_count"] >= 1


def test_상품_메인_썸네일_목록을_조회할_수_있다(
    get_products_with_thumbnails, sample_products_with_thumbnails
):
    """
    Given: 상품에 썸네일 이미지가 등록되어 있을 때
    When: 상품 목록을 조회하면
    Then: 썸네일 URL이 포함된다
    """
    # When
    response = get_products_with_thumbnails()

    # Then
    assert response.status_code == 200
    assert len(response.data["results"]) >= 1
    assert "thumbnail_url" in response.data["results"][0]
