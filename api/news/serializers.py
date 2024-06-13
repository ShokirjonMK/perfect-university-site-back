from rest_framework import serializers

from admin_panel.model import press_service
from api.serializers import ThumbnailImageSerializer


# don't change
class TitleSlugSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "slug": value.slug,
        }
        return obj


class TagSerializer(TitleSlugSerializer):
    pass


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.NewsCategory
        fields = ("id", "title", "slug")


class GallerySerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = press_service.Gallery
        fields = ("id", "image_url")


class ObjectiveShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.Objective
        fields = ("number", "color", "slug")


class ObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.Objective
        fields = ("number", "color", "slug", "title", "description", "icon")


class NewsListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title", required=False)
    category_slug = serializers.CharField(source="category.slug", required=False)
    hashtag = TagSerializer(many=True, read_only=True)
    gallery = serializers.SerializerMethodField()
    objectives = ObjectiveShortSerializer(many=True, read_only=True)

    # publish_date = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = press_service.News
        fields = [
            "id",
            "slug",
            "title",
            "views",
            "short_description",
            "thumbnail_url",
            "publish_date",
            "gallery",
            "category",
            "category_slug",
            "hashtag",
            "objectives"
        ]

    def get_gallery(self, obj):
        gallery_option = press_service.Gallery.objects.filter(news_id=obj.id)
        gallery = GallerySerializer(gallery_option, many=True).data
        return gallery


class TopNewsSerializer(NewsListSerializer):
    # category = serializers.CharField(source='category.title', required=False)
    # category_slug = serializers.CharField(source='category.slug',
    #                                       required=False)
    # hashtag = TagSerializer(many=True, read_only=True)

    # publish_date = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = press_service.News
        fields = [
            "id",
            "slug",
            "title",
            "views",
            "thumbnail_url",
            "publish_date",
            "category",
            "category_slug",
            "hashtag",
        ]


class NewsDetailSerializer(NewsListSerializer):
    # category = serializers.CharField(source='category.title', required=False)
    # category_slug = serializers.CharField(source='category.slug',
    #                                       required=False)
    # hashtag = TagSerializer(many=True, read_only=True)
    objectives = ObjectiveSerializer(many=True, read_only=True)
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = press_service.News
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "image_url",
            "views",
            "publish_date",
            "gallery",
            "category",
            "category_slug",
            "hashtag",
            "objectives"
        ]


#   _____ _             _
#  | ____| | ___  _ __ | | __ _ _ __
#  |  _| | |/ _ \| '_ \| |/ _` | '__|
#  | |___| | (_) | | | | | (_| | |
#  |_____|_|\___/|_| |_|_|\__,_|_|

# class ElonlarListSerializer(serializers.ModelSerializer):
#     # category = serializers.CharField(source='category.title', required=False)
#     # category_slug = serializers.CharField(source='category.slug', required=False)
#
#     class Meta:
#         model = press_service.Elonlar
#         fields = [
#             'id', 'title', 'views', 'thumbnail_url', 'publish_date',
#             # 'category', 'category_slug',
#         ]


# class TopElonlarSerializer(ElonlarListSerializer):
#     thumbnail_url = serializers.CharField(source='cover_url')


# class ElonlarDetailSerializer(serializers.ModelSerializer):
# category = serializers.CharField(source='category.title', required=False)
# category_slug = serializers.CharField(source='category.slug', required=False)
# hashtag = TagSerializer(many=True, read_only=True)

# class Meta:
#     model = press_service.Elonlar
#     fields = [
#         'id', 'title', 'description', 'image_url', 'views', 'publish_date',
#         # 'category', 'category_slug', 'hashtag',
#     ]


# class NewsCategoryserializer(serializers.ModelSerializer):
#     class Meta:
#         model = press_service.NewsCategory
#         fields = ['id', 'title', 'order', 'slug']


# class NewsHashtagserializer(serializers.ModelSerializer):
#     class Meta:
#         model = press_service.NewsHashtag
#         fields = ['id', 'title', 'slug']


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = press_service.FAQ
        fields = [
            "id",
            "title",
            "author",
        ]
