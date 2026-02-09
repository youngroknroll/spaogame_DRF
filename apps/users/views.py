from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .serializers import GenderChoiceSerializer, ProfileSerializer, SignUpSerializer

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class GenderListView(generics.GenericAPIView):
    """성별 목록 조회 (공개)"""

    serializer_class = GenderChoiceSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        choices = [{"value": value, "label": label} for value, label in User.Gender.choices]
        serializer = self.get_serializer(choices, many=True)
        return Response(serializer.data)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    프로필 조회 및 수정
    - GET: 본인 프로필 조회
    - PATCH: 본인 프로필 수정
    """

    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """현재 로그인한 사용자 반환"""
        return self.request.user
