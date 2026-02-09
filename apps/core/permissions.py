"""
공통 권한 클래스
"""

from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    조회(GET, HEAD, OPTIONS)는 누구나 가능
    생성/수정/삭제는 관리자만 가능
    """

    def has_permission(self, request, view):
        # 읽기 전용 요청(GET, HEAD, OPTIONS)은 모두 허용
        if request.method in SAFE_METHODS:
            return True

        # 그 외(POST, PUT, PATCH, DELETE)는 관리자만 허용
        return request.user and request.user.is_staff
