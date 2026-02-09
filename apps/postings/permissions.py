"""
Postings 앱 권한 클래스
"""

from rest_framework.permissions import BasePermission


class IsCommentOwner(BasePermission):
    """
    댓글 작성자만 수정/삭제 가능
    """

    message = "본인의 댓글만 삭제할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPostingOwner(BasePermission):
    """
    후기 작성자만 수정/삭제 가능
    """

    message = "본인의 후기만 수정/삭제할 수 있습니다."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
