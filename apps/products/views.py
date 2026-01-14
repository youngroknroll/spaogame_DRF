from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Menu
from .serializers import MenuSerializer


class MenuListView(generics.ListAPIView):
    """메뉴 목록 조회 (공개)"""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny]
