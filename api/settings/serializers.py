from rest_framework import serializers
from admin_panel.model import settings
from admin_panel.model import menu, ministry
from admin_panel.model import useful_link, courses
from django.db.models import Q
from api.serializers import ThumbnailImageSerializer


class TopLinkSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = settings.TopLink
        fields = ("id", "title", "link", "order", "child")

    def get_child(self, obj):
        top_link = settings.TopLink.objects.filter(parent=obj)
        if top_link.exists():
            return TopLinkSerializer(top_link, many=True).data
        return []


class HeaderSubMenuSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = ["id", "title", "url", "is_static"]

    def get_url(self, obj):
        if obj.is_static:
            return "static/" + obj.url
        else:
            return obj.url


class MenuSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            "id",
            "title",
            "description",
            "url",
            "child",
        ]

    def get_child(self, obj):
        sub_menu = menu.Menu.objects.filter(parent=obj, is_active=True, only_footer=False)
        if sub_menu.exists():
            return HeaderSubMenuSerializer(sub_menu, many=True).data
        return []


class FooterMenuSerializer(serializers.ModelSerializer):
    child = serializers.SerializerMethodField()

    class Meta:
        model = menu.Menu
        fields = [
            "id",
            "title",
            "description",
            "url",
            "child",
        ]

    def get_child(self, obj):
        sub_menu = menu.Menu.objects.filter(Q(footer=True) | Q(only_footer=True), parent=obj)
        if sub_menu.exists():
            return HeaderSubMenuSerializer(sub_menu, many=True).data
        return []


class RegionalDepartmentSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.title", required=False)
    region_id = serializers.CharField(source="region.id", required=False)

    class Meta:
        model = ministry.RegionalDepartment
        fields = [
            "id",
            "title",
            "address",
            "address_url",
            "director",
            "region",
            "region_id",
            "phone_number",
            "email",
        ]


class HeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = ["title", "logo_url", "logo_white_url", "quote", "quote_author", "phone_number", "address", "email"]


class RekvizitSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageSetting
        fields = [
            "title",
            "phone_number",
            "address",
            "email",
            "fax",
            "account_number",
            "bank",
            "mfo",
            "shxr",
            "inn",
            "okonx",
            "location",
        ]


class FooterSerializer(serializers.ModelSerializer):
    # updated_at = serializers.SerializerMethodField()

    class Meta:
        model = settings.MainPageSetting
        fields = [
            "title",
            "address",
            "logo_url",
            "logo_white_url",
            "email",
            "phone_number",
            "instagram",
            "facebook",
            "telegram",
            "twitter",
            "youtube",
            "linkedin",
            "support",
            "location",
            "footer_content",
        ]

    # def get_updated_at(self, obj):
    #     if settings.MainPageSetting.objects.last():
    #         return settings.MainPageSetting.objects.last().updated_at
    #     else:
    #         return ''


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = useful_link.UsefulLink
        fields = ["id", "url", "icon_url", "order"]


class SliderSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = settings.Slider
        fields = ("id", "title", "short_description", "image_url", "link", "order")


class MediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MediaImage
        fields = ["image"]


class SidebarSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = settings.Sidebar
        fields = ["title", "image_url", "link", "button_title"]


class MainPageDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.MainPageData
        fields = ["title", "description", "video_url", "is_active"]


class EntrantPageQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.EntrantPageQuestion
        fields = ("")