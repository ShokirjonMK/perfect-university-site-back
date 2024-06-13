# DJANGO MODULE
from django.conf import settings
from django.core.files.images import get_image_dimensions
from rest_framework import serializers
from sorl.thumbnail import get_thumbnail

# INTERNAL
from admin_panel.model import menu
from admin_panel.model import territorial
from admin_panel.model.settings import TopLink


class ThumbnailImageSerializer(serializers.Serializer):
    def __init__(self, *args, size_divider=None, quality=None, **kwargs):
        self.size_divider = size_divider
        self.quality = quality
        super().__init__(*args, **kwargs)

    def _build_absolute_uri(self, path):
        if not settings.USE_HOST:
            self.request = self.context.get("request")
            if self.request is not None:
                return self.request.build_absolute_uri(path)
        return "{}{}".format(settings.HOST, path)

    def _needs_compression(self, image):
        return (image.size // 1024) > 1024

    def to_representation(self, image):
        if not image:
            return ""

        if self._needs_compression(image):
            size_divider = self.size_divider or 2
            quality = self.quality or 90

            width, height = get_image_dimensions(image)
            if width and height:
                return self._build_absolute_uri(
                    get_thumbnail(
                        image, f"{int(width // size_divider)}x{int(height // size_divider)}", quality=quality
                    ).url
                )

        return self._build_absolute_uri(image.url)


# MENU --> CHILD


class SubMenuSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = ["id", "title", "link", "slug", "order", "is_static"]

    def get_link(self, obj):
        if obj.is_static:
            return "page/" + obj.url
        else:
            return obj.url


class SubTopLinkSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = TopLink
        fields = ["id", "title_uz", "title_ru", "title_en", "link", "order"]

    def get_link(self, obj):
        return obj.link


# MENU --> PARENT
class MenuSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            "id",
            "title_uz",
            "title_ru",
            "title_en",
            "url",
            "slug",
            "child",
        ]

    def get_child(self, obj):
        sub_menu = menu.Menu.objects.filter(parent=obj)
        if sub_menu.exists():
            return SubMenuSerializer(sub_menu, many=True).data
        return []


# MENU --> PARENT
class TopLinkSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = TopLink
        fields = ["title_uz", "title_ru", "title_en", "link", "child", "order"]

    def get_child(self, obj):
        sub_menu = TopLink.objects.filter(parent=obj).order_by("order")
        if sub_menu.exists():
            return SubTopLinkSerializer(sub_menu, many=True).data
        return []


class StaticMenuSerializer(serializers.ModelSerializer):
    # link = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = ["id", "title", "url", "is_static"]

    # def get_link(self, obj):
    #     return  obj.link


# REGION
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = territorial.Region
        fields = ["id", "title"]
