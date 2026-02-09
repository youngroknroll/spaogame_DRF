"""
댓글 테스트
"""


def test_사용자는_특정_후기의_댓글_목록을_조회할_수_있다(
    create_posting, create_comment, api_client, sample_product
):
    """
    Given: 후기에 여러 개의 댓글이 있을 때
    When: 댓글 목록을 조회하면
    Then: 모든 댓글이 조회된다
    """
    from apps.conftest import API_COMMENTS

    # Given - 후기 작성
    posting_response = create_posting(
        sample_product.id,
        {"title": "맛있어요!", "content": "정말 맛있게 잘 먹었습니다.", "rating": 5},
    )
    posting_id = posting_response.data["id"]

    # 댓글 3개 작성
    create_comment(posting_id, {"content": "첫 번째 댓글"})
    create_comment(posting_id, {"content": "두 번째 댓글"})
    create_comment(posting_id, {"content": "세 번째 댓글"})

    # When - 댓글 목록 조회
    url = API_COMMENTS.format(posting_id=posting_id)
    response = api_client.get(url)

    # Then
    assert response.status_code == 200
    assert response.data["count"] == 3
    assert len(response.data["results"]) == 3
    assert response.data["results"][0]["content"] == "첫 번째 댓글"
    assert response.data["results"][1]["content"] == "두 번째 댓글"
    assert response.data["results"][2]["content"] == "세 번째 댓글"


def test_인증_로그인한_사용자는_후기에_댓글을_작성할_수_있다(
    create_posting, create_comment, sample_product
):
    """
    Given: 로그인한 사용자와 후기가 있을 때
    When: 댓글을 작성하면
    Then: 댓글이 생성된다
    """
    # Given - 후기 작성
    posting_response = create_posting(
        sample_product.id,
        {"title": "맛있어요!", "content": "정말 맛있게 잘 먹었습니다.", "rating": 5},
    )
    posting_id = posting_response.data["id"]

    # When - 댓글 작성
    comment_payload = {"content": "저도 먹어보고 싶네요!"}
    response = create_comment(posting_id, comment_payload)

    # Then
    assert response.status_code == 201
    assert response.data["content"] == "저도 먹어보고 싶네요!"


def test_권한_댓글_작성자는_자신의_댓글을_삭제할_수_있다(
    create_posting, create_comment, delete_comment, sample_product
):
    """
    Given: 자신이 작성한 댓글이 있을 때
    When: 댓글을 삭제하면
    Then: 댓글이 삭제된다
    """
    # Given - 후기 및 댓글 작성
    posting_response = create_posting(
        sample_product.id,
        {"title": "맛있어요!", "content": "정말 맛있게 잘 먹었습니다.", "rating": 5},
    )
    posting_id = posting_response.data["id"]

    comment_response = create_comment(posting_id, {"content": "좋은 후기!"})
    comment_id = comment_response.data["id"]

    # When - 댓글 삭제
    response = delete_comment(posting_id, comment_id)

    # Then
    assert response.status_code == 204


def test_권한_댓글_작성자가_아닌_사용자는_댓글을_삭제할_수_없다(
    create_posting, create_comment, sample_product, api_client, db
):
    """
    Given: 다른 사용자가 작성한 댓글이 있을 때
    When: 다른 사용자가 댓글을 삭제하려고 하면
    Then: 권한 오류가 발생한다
    """
    from django.contrib.auth import get_user_model

    from apps.conftest import ADMIN_EMAIL, ADMIN_PASSWORD, API_COMMENT, API_USERS_LOGIN

    User = get_user_model()

    # Given - 첫 번째 사용자가 후기와 댓글 작성
    posting_response = create_posting(
        sample_product.id,
        {"title": "맛있어요!", "content": "정말 맛있게 잘 먹었습니다.", "rating": 5},
    )
    posting_id = posting_response.data["id"]

    comment_response = create_comment(posting_id, {"content": "좋은 후기!"})
    comment_id = comment_response.data["id"]

    # 두 번째 사용자(admin) 로그인
    _admin_user = User.objects.create_user(
        email=ADMIN_EMAIL,
        password=ADMIN_PASSWORD,
        name="관리자",
        is_staff=True,
    )
    login_response = api_client.post(
        API_USERS_LOGIN,
        {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
        },
    )
    admin_token = login_response.data["access"]
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {admin_token}")

    # When - 다른 사용자의 댓글을 삭제하려고 시도
    url = API_COMMENT.format(posting_id=posting_id, comment_id=comment_id)
    response = api_client.delete(url)

    # Then - 403 권한 오류 발생
    assert response.status_code == 403
