from rest_framework import serializers
from admin_panel.model import service


class ServiceTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = service.Service
        fields = ["id", "title", "content", "order", "icon_url", "white_icon_url", "url"]


class ServiceSerializer(serializers.ModelSerializer):
    # icon_url = serializers.URLField(source='main_icon_url')
    class Meta:
        model = service.Service
        fields = ["id", "title", "content", "order", "icon_url", "white_icon_url", "url"]
