"""
Postings 앱 뷰 (FBV 방식)
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Posting, Comment
from .serializers import PostingSerializer, CommentSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def posting_create(request, product_id):
    """
    후기 작성
    - 로그인 필수
    """
    serializer = PostingSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, product_id=product_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_create(request, posting_id):
    """
    댓글 작성
    - 로그인 필수
    """
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user, posting_id=posting_id)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comment_delete(request, posting_id, comment_id):
    """
    댓글 삭제
    - 본인이 작성한 댓글만 삭제 가능
    """
    try:
        comment = Comment.objects.get(id=comment_id, posting_id=posting_id)
    except Comment.DoesNotExist:
        return Response(
            {"error": "댓글을 찾을 수 없습니다."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # 권한 검증: 본인의 댓글인지 확인
    if comment.user != request.user:
        return Response(
            {"error": "본인의 댓글만 삭제할 수 있습니다."},
            status=status.HTTP_403_FORBIDDEN
        )
    
    comment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
