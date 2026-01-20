from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    """회원가입 시리얼라이저 (확장 필드 포함)"""
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email", "password", "name",
            "username", "mobile_number", 
            "address1", "address2", 
            "birthday", "gender"
        ]

    def validate_email(self, value):
        """이메일 정규화 (소문자 변환)"""
        return value.lower()

    def validate_password(self, value):
        """비밀번호 검증"""
        validate_password(value)
        return value
    
    def validate_gender(self, value):
        """성별 검증"""
        if value and value not in ["M", "F"]:
            raise serializers.ValidationError("성별은 M(남성) 또는 F(여성)이어야 합니다.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class GenderChoiceSerializer(serializers.Serializer):
    """성별 선택지 응답 시리얼라이저"""
    value = serializers.CharField()
    label = serializers.CharField()
