from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .serializers import SignUpSerializer, GenderChoiceSerializer

User = get_user_model()


class SignUpView(generics.CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]


class GenderListView(generics.GenericAPIView):
    """성별 목록 조회 (공개)"""
    serializer_class = GenderChoiceSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        choices = [
            {"value": value, "label": label}
            for value, label in User.Gender.choices
        ]
        serializer = self.get_serializer(choices, many=True)
        return Response(serializer.data)
