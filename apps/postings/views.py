"""
Postings 앱 뷰 (CBV 방식)
"""
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import Product
from .models import Posting, Comment
from .serializers import (
    PostingSerializer,
    PostingCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
)
from .permissions import IsCommentOwner


class PostingCreateView(generics.CreateAPIView):
    """
    후기 작성
    - POST: 로그인 필수
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostingCreateSerializer

    def create(self, request, *args, **kwargs):
        """후기 생성"""
        product = get_object_or_404(Product, id=self.kwargs['product_id'])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        posting = Posting.objects.create(
            user=request.user,
            product=product,
            **serializer.validated_data
        )
        
        response_serializer = PostingSerializer(posting)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CommentCreateView(generics.CreateAPIView):
    """
    댓글 작성
    - POST: 로그인 필수
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        """댓글 생성"""
        posting = get_object_or_404(Posting, id=self.kwargs['posting_id'])
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        comment = Comment.objects.create(
            user=request.user,
            posting=posting,
            **serializer.validated_data
        )
        
        response_serializer = CommentSerializer(comment)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class CommentDeleteView(generics.DestroyAPIView):
    """
    댓글 삭제
    - DELETE: 본인이 작성한 댓글만 삭제 가능
    """
    permission_classes = [IsAuthenticated, IsCommentOwner]
    queryset = Comment.objects.all()
    lookup_url_kwarg = "comment_id"

    def get_queryset(self):
        """해당 posting의 댓글만 필터링"""
        return Comment.objects.filter(posting_id=self.kwargs['posting_id'])
