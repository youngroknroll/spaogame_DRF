"""
Postings 앱 시리얼라이저
"""

from rest_framework import serializers

from .models import Comment, Posting


class PostingSerializer(serializers.ModelSerializer):
    """후기 시리얼라이저 (응답용)"""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Posting
        fields = [
            "id",
            "product",
            "user",
            "user_email",
            "title",
            "content",
            "rating",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "product", "created_at", "updated_at"]


class PostingCreateSerializer(serializers.Serializer):
    """후기 작성 시리얼라이저 (입력용)"""

    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    rating = serializers.IntegerField(min_value=1, max_value=5)


class CommentSerializer(serializers.ModelSerializer):
    """댓글 시리얼라이저 (응답용)"""

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "posting", "user", "user_email", "content", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "posting", "created_at", "updated_at"]


class CommentCreateSerializer(serializers.Serializer):
    """댓글 작성 시리얼라이저 (입력용)"""

    content = serializers.CharField()
