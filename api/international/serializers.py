from rest_framework import serializers
from admin_panel.model import international
from api.serializers import ThumbnailImageSerializer


class FileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {"id": value.id, "title": value.title, "file_url": value.file_url}
        return obj


class OnlyFileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {"file_name": value.file_name, "file_type": value.file_type, "file_url": value.file_url}
        return obj


class GrantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.Grant
        fields = ("id", "title", "short_description", "publish_date", "slug", "views")


class GrantDetailSerializer(serializers.ModelSerializer):
    files = OnlyFileSerializer(many=True, read_only=True)

    class Meta:
        model = international.Grant
        fields = ["id", "slug", "title", "image_url", "description", "views", "publish_date", "files"]


# international.InternationalConference
class ConferencePagesSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "department": value.department,
            "date": value.date,
            "place": value.place,
            # 'page_link': value.page_link,
        }
        return obj


class InternationalConferencePageSerializer(serializers.ModelSerializer):
    # conferences = ConferencePagesSerializer(many=True, read_only=True)
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.InternationalConferencePage
        fields = (
            "id",
            "title",
            "content",
            "image_url",
        )


class InternationalRelationSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.InternationalRelation
        fields = ("id", "title", "image_url", "short_description", "link")


class InternationalStaffSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.InternationalStaff
        fields = ("title", "image_url", "place", "short_description")


class InternationalUsufulLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.InternationalRelation
        fields = ("title", "link")


class InternationalPartnerPageSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.InternationalPartnerPage
        fields = ("title", "content", "views", "image_url", "date")


class InternationalPartnerSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.InternationalPartner
        fields = ("image_url", "url")


# Sirtqi bo'lim serializer
class ExternalSectionListSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.ExternalSection
        fields = ("id", "title", "content", "image_url", "created_at", "updated_at")


class ExternalSectionDetailSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = international.ExternalSection
        fields = ("id", "title", "content", "image_url", "created_at", "updated_at")


class InternationalFacultyPageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.InternationalFacultyPage
        fields = (
            "id",
            "title",
            "content",
            "video_url",
        )


class InternationalFacultyApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.InternationalFacultyApplication
        fields = (
            "id",
            "full_name",
            "category",
            "passport_front",
            "passport_back",
            "image_3_4",
            "birth_date",
            "address",
            "phone_number1",
            "phone_number2",
            "school_number",
        )


class InternationalCooperationCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.InternationalCooperationCategory
        fields = ("id", "title", "slug")


class InternationalCooperationModelSerializer(serializers.ModelSerializer):
    category = InternationalCooperationCategoryModelSerializer(read_only=True)

    class Meta:
        model = international.InternationalCooperation
        fields = ("id", "title", "image_url", "content", "category", "link")


class RankingModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.Ranking
        fields = (
            "id",
            "image",
            "reputation_ranking",
            "academic_reputation_ranking",
            "employer_reputation_ranking",
            "reputation_assessment"
        )


class JointProgramsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = international.JointPrograms
        fields = (
            "id",
            "title",
            "image",
            "link",
            "order"
        )
