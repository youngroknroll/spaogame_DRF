from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "name"]

    def validate_password(self, value):
        """비밀번호 검증"""
        validate_password(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
