from rest_framework import serializers

from admin_panel.model import event, press_service, static


class VebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.Vebinar
        fields = ("id", "title", "created_at")


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = event.Event
        fields = ("id", "title", "created_at")


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.News
        fields = ("id", "title", "slug", "created_at")


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.PhotoGallery
        fields = ("id", "title", "created_at")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.VideoGallery
        fields = ("id", "title", "created_at")


class StaticSerializer(serializers.ModelSerializer):
    class Meta:
        model = static.StaticPage
        fields = ("id", "title", "url", "slug", "created_at")


class SearchSerializer(serializers.Serializer):
    events = EventSerializer(many=True)
    news = NewsSerializer(many=True)
    photogallery = PhotoSerializer(many=True)
    videogallery = VideoSerializer(many=True)
    vebinar = VebinarSerializer(many=True)
    # static_page = StaticSerializer(many=True)
