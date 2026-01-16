"""
Postings 앱 시리얼라이저
"""
from rest_framework import serializers
from .models import Posting, Comment


class PostingSerializer(serializers.ModelSerializer):
    """후기 시리얼라이저"""
    user_email = serializers.EmailField(source="user.email", read_only=True)
    
    class Meta:
        model = Posting
        fields = ["id", "product", "user", "user_email", "title", "content", "rating", "created_at", "updated_at"]
        read_only_fields = ["user", "product"]


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저"""
    user_email = serializers.EmailField(source="user.email", read_only=True)
    
    class Meta:
        model = Comment
        fields = ["id", "posting", "user", "user_email", "content", "created_at", "updated_at"]
        read_only_fields = ["user", "posting"]
