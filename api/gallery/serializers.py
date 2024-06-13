from rest_framework import serializers

from admin_panel.model import press_service


class GalleryImageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "src": value.url,
        }
        return obj


class PhotoSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField(source="images.count", read_only=True, required=False)

    class Meta:
        model = press_service.PhotoGallery
        fields = [
            "id",
            "title",
            "thumbnail_url",
            "publish_date",
            "count",
        ]


class PhotoDetailSerializer(serializers.ModelSerializer):
    images = GalleryImageSerializer(many=True, read_only=True)

    class Meta:
        model = press_service.PhotoGallery
        fields = [
            "id",
            "title",
            "publish_date",
            "images",
        ]


class VideoSerializer(serializers.ModelSerializer):
    src = serializers.URLField(source="video_link")

    class Meta:
        model = press_service.VideoGallery
        fields = ["id", "title", "thumb", "src", "publish_date", "views"]


class VideoDetailSerializer(serializers.ModelSerializer):
    src = serializers.URLField(source="video_link")

    class Meta:
        model = press_service.VideoGallery
        fields = ["id", "title", "description", "thumb", "src", "publish_date", "views"]


class VebinarSerializer(serializers.ModelSerializer):
    src = serializers.URLField(source="video_link")

    class Meta:
        model = press_service.Vebinar
        fields = [
            "id",
            "title",
            "author",
            "thumb",
            "src",
            "publish_date",
        ]
