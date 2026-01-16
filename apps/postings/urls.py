"""
Postings 앱 URL 라우팅
"""
from django.urls import path
from . import views

urlpatterns = [
    # 후기
    path("products/<int:product_id>/postings/", views.posting_create, name="posting-create"),
    
    # 댓글
    path("postings/<int:posting_id>/comments/", views.comment_create, name="comment-create"),
    path("postings/<int:posting_id>/comments/<int:comment_id>/", views.comment_delete, name="comment-delete"),
]
