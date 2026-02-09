"""
Postings 도메인 비즈니스 로직

Service Layer는 비즈니스 규칙과 트랜잭션 경계를 담당합니다.
View는 HTTP 처리만, Service는 도메인 로직만 담당합니다.
"""

import logging

from django.db import transaction
from django.shortcuts import get_object_or_404

from apps.products.models import Product

from .models import Comment, Posting

logger = logging.getLogger(__name__)


class PostingService:
    """후기 비즈니스 로직"""

    @staticmethod
    @transaction.atomic
    def create_posting(user, product_id, title, content, rating):
        """
        후기 생성

        Args:
            user: 작성자
            product_id: 상품 ID
            title: 제목
            content: 내용
            rating: 평점 (1-5)

        Returns:
            Posting: 생성된 후기
        """
        logger.info(
            f"후기 생성 시도: user={user.email}, product_id={product_id}, "
            f"title={title}, rating={rating}"
        )

        product = get_object_or_404(Product, id=product_id)

        posting = Posting.objects.create(
            user=user, product=product, title=title, content=content, rating=rating
        )

        logger.info(
            f"후기 생성 완료: user={user.email}, posting_id={posting.id}, product_id={product_id}"
        )

        return posting

    @staticmethod
    @transaction.atomic
    def update_posting(user, posting_id, **kwargs):
        """
        후기 수정

        Args:
            user: 요청 사용자
            posting_id: 후기 ID
            **kwargs: 수정할 필드들

        Returns:
            Posting: 수정된 후기

        Raises:
            PermissionDenied: 작성자가 아닌 경우 (403)
        """
        from rest_framework.exceptions import PermissionDenied

        logger.info(f"후기 수정 시도: user={user.email}, posting_id={posting_id}")

        posting = get_object_or_404(Posting, id=posting_id)

        # 권한 검증: Service Layer에서 수행
        if posting.user != user:
            logger.warning(
                f"후기 수정 권한 없음: user={user.email}, "
                f"posting_owner={posting.user.email}, posting_id={posting_id}"
            )
            raise PermissionDenied("본인의 후기만 수정할 수 있습니다.")

        for key, value in kwargs.items():
            if hasattr(posting, key) and value is not None:
                setattr(posting, key, value)

        posting.save()

        logger.info(f"후기 수정 완료: posting_id={posting_id}")

        return posting

    @staticmethod
    @transaction.atomic
    def delete_posting(user, posting_id):
        """
        후기 삭제

        Args:
            user: 요청 사용자
            posting_id: 후기 ID

        Raises:
            PermissionDenied: 작성자가 아닌 경우 (403)
        """
        from rest_framework.exceptions import PermissionDenied

        logger.info(f"후기 삭제 시도: user={user.email}, posting_id={posting_id}")

        posting = get_object_or_404(Posting, id=posting_id)

        # 권한 검증: Service Layer에서 수행
        if posting.user != user:
            logger.warning(
                f"후기 삭제 권한 없음: user={user.email}, "
                f"posting_owner={posting.user.email}, posting_id={posting_id}"
            )
            raise PermissionDenied("본인의 후기만 삭제할 수 있습니다.")

        posting.delete()

        logger.info(f"후기 삭제 완료: posting_id={posting_id}")


class CommentService:
    """댓글 비즈니스 로직"""

    @staticmethod
    @transaction.atomic
    def create_comment(user, posting_id, content):
        """
        댓글 생성

        Args:
            user: 작성자
            posting_id: 후기 ID
            content: 댓글 내용

        Returns:
            Comment: 생성된 댓글
        """
        logger.info(f"댓글 생성 시도: user={user.email}, posting_id={posting_id}")

        posting = get_object_or_404(Posting, id=posting_id)

        comment = Comment.objects.create(user=user, posting=posting, content=content)

        logger.info(
            f"댓글 생성 완료: user={user.email}, comment_id={comment.id}, posting_id={posting_id}"
        )

        return comment

    @staticmethod
    @transaction.atomic
    def delete_comment(user, posting_id, comment_id):
        """
        댓글 삭제

        Args:
            user: 요청 사용자
            posting_id: 후기 ID
            comment_id: 댓글 ID

        Raises:
            PermissionDenied: 작성자가 아닌 경우 (403)
        """
        from rest_framework.exceptions import PermissionDenied

        logger.info(
            f"댓글 삭제 시도: user={user.email}, posting_id={posting_id}, comment_id={comment_id}"
        )

        comment = get_object_or_404(Comment, id=comment_id, posting_id=posting_id)

        # 권한 검증: Service Layer에서 수행
        if comment.user != user:
            logger.warning(
                f"댓글 삭제 권한 없음: user={user.email}, "
                f"comment_owner={comment.user.email}, comment_id={comment_id}"
            )
            raise PermissionDenied("본인의 댓글만 삭제할 수 있습니다.")

        comment.delete()

        logger.info(f"댓글 삭제 완료: comment_id={comment_id}")
