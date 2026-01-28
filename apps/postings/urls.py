"""
Postings 앱 URL 라우팅
"""
from django.urls import path
from .views import (
    PostingListView,
    PostingDetailView,
    PostingCreateView,
    CommentCreateView,
    CommentDeleteView,
)

urlpatterns = [
    # 후기 목록 및 상세
    path("postings/", PostingListView.as_view(), name="posting-list"),
    path("postings/<int:posting_id>/", PostingDetailView.as_view(), name="posting-detail"),

    # 후기 작성
    path("products/<int:product_id>/postings/", PostingCreateView.as_view(), name="posting-create"),

    # 댓글
    path("postings/<int:posting_id>/comments/", CommentCreateView.as_view(), name="comment-create"),
    path("postings/<int:posting_id>/comments/<int:comment_id>/", CommentDeleteView.as_view(), name="comment-delete"),
]
