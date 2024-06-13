from rest_framework import serializers

from admin_panel.model import menu
from admin_panel.model import static
from api.settings import serializers as menu_serializer


class ImageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            'id': value.id,
            'image_url': value.url
        }
        return obj


class StaticSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = static.StaticPage
        fields = [
            'id', 'title', 'url', 'slug', 'views', 'active', 'content', 'images', 'date'
        ]


class StaticMenuSerializer(menu_serializer.HeaderSubMenuSerializer):
    class Meta:
        model = menu.Menu
        fields = [
            'id', 'title', 'url', 'is_static'
        ]

