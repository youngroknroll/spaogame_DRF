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
    path("", PostingListView.as_view(), name="posting-list"),
    path("<int:posting_id>/", PostingDetailView.as_view(), name="posting-detail"),

    # 댓글
    path("<int:posting_id>/comments/", CommentCreateView.as_view(), name="comment-create"),
    path("<int:posting_id>/comments/<int:comment_id>/", CommentDeleteView.as_view(), name="comment-delete"),
]
