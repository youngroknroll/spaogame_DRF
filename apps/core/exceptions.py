"""
커스텀 예외 처리

통일된 에러 응답 형식을 제공합니다.
"""

from rest_framework.exceptions import (
    AuthenticationFailed,
    MethodNotAllowed,
    NotAuthenticated,
    NotFound,
    PermissionDenied,
    Throttled,
    ValidationError,
)
from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """
    통일된 에러 응답 형식

    응답 포맷:
    {
        "success": false,
        "error": {
            "code": "validation_error",
            "message": "입력 데이터가 유효하지 않습니다.",
            "details": {...}
        }
    }
    """
    # DRF 기본 예외 처리 먼저 실행
    response = drf_exception_handler(exc, context)

    if response is not None:
        # 에러 코드 매핑
        error_code = _get_error_code(exc)
        error_message = _get_error_message(exc)

        # 통일된 응답 형식
        custom_response = {
            "success": False,
            "error": {"code": error_code, "message": error_message, "details": response.data},
        }
        response.data = custom_response

    return response


def _get_error_code(exc):
    """예외 타입별 에러 코드"""
    error_code_map = {
        ValidationError: "validation_error",
        NotFound: "not_found",
        PermissionDenied: "permission_denied",
        AuthenticationFailed: "authentication_failed",
        NotAuthenticated: "not_authenticated",
        MethodNotAllowed: "method_not_allowed",
        Throttled: "throttled",
    }
    return error_code_map.get(type(exc), "unknown_error")


def _get_error_message(exc):
    """예외 타입별 메시지"""
    if isinstance(exc, ValidationError):
        return "입력 데이터가 유효하지 않습니다."
    elif isinstance(exc, NotFound):
        return "요청한 리소스를 찾을 수 없습니다."
    elif isinstance(exc, PermissionDenied):
        return "접근 권한이 없습니다."
    elif isinstance(exc, AuthenticationFailed):
        return "인증에 실패했습니다."
    elif isinstance(exc, NotAuthenticated):
        return "인증이 필요합니다."
    elif isinstance(exc, MethodNotAllowed):
        return "허용되지 않은 HTTP 메서드입니다."
    elif isinstance(exc, Throttled):
        return "요청이 너무 많습니다. 잠시 후 다시 시도해주세요."
    else:
        return str(exc)
