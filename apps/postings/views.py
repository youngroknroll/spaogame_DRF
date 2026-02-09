"""
Postings 앱 뷰 (CBV 방식)
"""

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comment, Posting
from .serializers import (
    CommentCreateSerializer,
    CommentSerializer,
    PostingCreateSerializer,
    PostingSerializer,
)
from .services import CommentService, PostingService


class PostingListView(generics.ListAPIView):
    """
    후기 목록 조회 (공개)
    - GET: 누구나 조회 가능
    """

    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    permission_classes = [AllowAny]


class PostingDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    후기 상세 조회/수정/삭제
    - GET: 누구나 조회 가능
    - PATCH/DELETE: 로그인 필수, 권한 검증은 Service에서 수행
    """

    queryset = Posting.objects.all()
    serializer_class = PostingSerializer
    lookup_url_kwarg = "posting_id"

    def get_permissions(self):
        """GET은 AllowAny, PATCH/DELETE는 인증만 (권한은 Service에서)"""
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def update(self, request, *args, **kwargs):
        """후기 수정 (Service Layer에 위임)"""
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        posting = PostingService.update_posting(
            user=request.user, posting_id=kwargs["posting_id"], **serializer.validated_data
        )

        response_serializer = self.get_serializer(posting)
        return Response(response_serializer.data)

    def destroy(self, request, *args, **kwargs):
        """후기 삭제 (Service Layer에 위임)"""
        PostingService.delete_posting(user=request.user, posting_id=kwargs["posting_id"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostingCreateView(generics.CreateAPIView):
    """
    후기 작성
    - POST: 로그인 필수
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostingCreateSerializer

    def create(self, request, *args, **kwargs):
        """후기 생성"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service에 위임
        posting = PostingService.create_posting(
            user=request.user, product_id=self.kwargs["product_id"], **serializer.validated_data
        )

        response_serializer = PostingSerializer(posting)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CommentListCreateView(generics.ListCreateAPIView):
    """
    댓글 목록 조회 및 생성
    - GET: 누구나 조회 가능
    - POST: 로그인 필수
    """

    serializer_class = CommentSerializer

    def get_permissions(self):
        """GET은 AllowAny, POST는 인증 필요"""
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """특정 후기의 댓글 목록 조회"""
        return (
            Comment.objects.filter(posting_id=self.kwargs["posting_id"])
            .select_related("user")
            .order_by("created_at")
        )

    def get_serializer_class(self):
        """GET은 CommentSerializer, POST는 CommentCreateSerializer"""
        if self.request.method == "POST":
            return CommentCreateSerializer
        return CommentSerializer

    def create(self, request, *args, **kwargs):
        """댓글 생성"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Service에 위임
        comment = CommentService.create_comment(
            user=request.user, posting_id=self.kwargs["posting_id"], **serializer.validated_data
        )

        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    """
    댓글 삭제
    - DELETE: 로그인 필수, 권한 검증은 Service에서 수행
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def destroy(self, request, *args, **kwargs):
        """댓글 삭제 (Service Layer에 위임)"""
        # Service에서 권한 검증 + 삭제 수행
        CommentService.delete_comment(
            user=request.user, posting_id=kwargs["posting_id"], comment_id=kwargs["comment_id"]
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
