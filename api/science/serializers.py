from rest_framework import serializers
from api.news.serializers import TitleSlugSerializer
from admin_panel.model import science


class SectionSerializer(serializers.Serializer):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            # 'section_number': value.section_number,
            "title": value.title,
            "author": value.author,
            "file_url": value.file_url,
        }
        return obj


class MonoFileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {"id": value.id, "title": value.title, "file_url": value.file_url}
        return obj


class MonoArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.MonoArticle
        fields = ("id", "title", "slug")


class MonoArticleDetailSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()
    mono_files = MonoFileSerializer(many=True, read_only=True)

    class Meta:
        model = science.MonoArticle
        fields = ("id", "title", "slug", "mono_files", "section")

    def get_section(self, obj):
        return [
            {
                "section_number": i,
                "data": [
                    {"id": value.id, "title": value.title, "author": value.author, "file_url": value.file_url}
                    for value in obj.sections.filter(section_number=i)
                ],
            }
            for i in obj.sections.values_list("section_number", flat=True).distinct("section_number")
        ]

    # def to_representation(self, obj):
    #     rep = super(MonoArticleDetailSerializer, self).to_representation(obj)
    #     rep['sections'] =
    #
    #     return rep


class YearlyConferenceSubjectSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(format=None)
    end_date = serializers.DateField(format=None)

    class Meta:
        model = science.ConferenceSubject
        fields = ["id", "title", "department", "file_url", "place", "date", "start_date", "end_date"]


class YearlyConferencesSerializer(serializers.ModelSerializer):
    subjects = YearlyConferenceSubjectSerializer(many=True)

    class Meta:
        model = science.Conference
        fields = ["title", "subjects"]


class ConferenceTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.ConferenceTags
        fields = ["id", "name"]


class ConferenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.PendingConference
        fields = ["id", "title", "description", "date", "start_time", "end_time", "icon", "slug", "status"]


class ConferenceDetailSerializer(serializers.ModelSerializer):
    tags = ConferenceTagsSerializer(many=True)

    class Meta:
        model = science.PendingConference
        fields = [
            "id",
            "title",
            "description",
            "date",
            "start_time",
            "end_time",
            "icon",
            "views",
            "status",
            "image",
            "tags",
            "created_at",
        ]


class ConferenceApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.ConferenceApplication
        fields = ["id", "full_name", "phone_number", "addition_phone_number", "email", "file", "conference"]


class ConferenceSubjectSerializer(serializers.BaseSerializer):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "department": value.department,
            "file_url": value.file_url,
            "place": value.place,
            "date": value.date,
        }
        return obj


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.Conference
        fields = ("id", "title")


class ScienceFilesSerailizer(serializers.ModelSerializer):
    class Meta:
        model = science.ScienceFiles
        fields = ("id", "title", "file_name", "file_url")


class ScienceNewsListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title", required=False)
    category_slug = serializers.CharField(source="category.slug", required=False)
    hashtag = TitleSlugSerializer(many=True, read_only=True)

    class Meta:
        model = science.ScienceNews
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


class ScienceNewsDetailSerializer(ScienceNewsListSerializer):
    class Meta:
        model = science.ScienceNews
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "image_url",
            "views",
            "publish_date",
            "category",
            "category_slug",
            "hashtag",
        ]


class SeminarListSerializer(ScienceNewsListSerializer):
    class Meta:
        model = science.Seminar
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


class SeminarRelatedListSerializer(ScienceNewsListSerializer):
    class Meta:
        model = science.Seminar
        fields = ["id", "slug", "title", "thumbnail_url", "publish_date", "category", "category_slug"]


class SeminarDetailSerializer(SeminarListSerializer):
    class Meta:
        model = science.Seminar
        fields = [
            "id",
            "slug",
            "title",
            "description",
            "image_url",
            "views",
            "publish_date",
            "category",
            "category_slug",
            "hashtag",
        ]


class ScienceCenterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.ScienceCenter
        fields = ("id", "title", "description", "slug")


class ScienceCenterSingleSerializer(serializers.ModelSerializer):
    class Meta:
        model = science.ScienceCenter
        fields = ("id", "title", "description", "phone_number", "email", "fax", "reception_time")
