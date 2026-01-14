from rest_framework import serializers

from .models import Menu


class MenuSerializer(serializers.ModelSerializer):
    """메뉴 시리얼라이저"""
    
    class Meta:
        model = Menu
        fields = ["id", "name", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
