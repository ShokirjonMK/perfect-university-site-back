from rest_framework import serializers

from admin_panel.model import ministry, settings
from api.serializers import ThumbnailImageSerializer



class RectorCongratulationSerializer(serializers.ModelSerializer):
    # image_url = ThumbnailImageSerializer(source="image", read_only=True)
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = ministry.RectorCongratulation
        fields = [
            "date",
            "content",
            "rector_fullname",
            "image_url",
            "title",
            "instagram",
            "facebook",
            "linkedin",
        ]
    
    def get_image_url(self, obj):
        return obj.rector_image


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.AboutMinistry
        fields = ["title", "content", "image_urls"]


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Goal
        fields = ["title", "content", "views", "created_at"]


class StructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Structure
        fields = [
            "id",
            "title",
            "content",
            "views",
            "type",
        ]


class DepartmentSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.Department
        fields = ["id", "title", "image_url", "slug", "description", "link"]


class DepartmentStaffSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True, size_divider=1)

    class Meta:
        model = ministry.Staff
        fields = [
            "id",
            "title",
            "order",
            "position",
            "reception_days",
            "duty",
            "work_history",
            "phone_number",
            "email",
            "fax",
            "image_url",
            "department",
            "kafedra",
            "organization",
            "main",
            "leader",
            "rector",
            "updated_at",
            "created_at",
        ]


class DepartmentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Department
        fields = [
            "kafedras",
            "directions",
            "history",
            "study_works",
            "spiritual_directions",
            "research_works",
            "innovative_works",
            "faculty_innovative_works",
            "cooperation",
            "international_relations",
            "faculty_international_relations",
            "slug",
            "link",
        ]


class StaffListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Staff
        fields = ["id", "title", "position", "phone_number", "reception_days", "email", "fax", "image_url", "rector"]


class DepartmentInfoInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.DepartmentInfo
        fields = ["id", "title", "content", "order", "updated_at", "created_at"]


class DepartmentAdminInfoInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.DepartmentInfo
        fields = [
            "id",
            "department",
            "title_uz",
            "title_sr",
            "title_en",
            "title_ru",
            "content_uz",
            "content_sr",
            "content_en",
            "content_ru",
            "order",
        ]


class DepartmentDetailSerializer(serializers.ModelSerializer):
    info = DepartmentInfoInlineSerializer(many=True)
    staffs = StaffListSerializer(many=True)
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.Department
        fields = [
            "id",
            "title",
            "image_url",
            "slug",
            "kafedras",
            "directions",
            "history",
            "study_works",
            "spiritual_directions",
            "research_works",
            "innovative_works",
            "faculty_innovative_works",
            "cooperation",
            "international_relations",
            "faculty_international_relations",
            "slug",
            "staffs",
            "info",
        ]


class StaffSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True, size_divider=2, quality=90)

    class Meta:
        model = ministry.Staff
        fields = [
            "id",
            "title",
            "position",
            "phone_number",
            "reception_days",
            "work_history",
            "instagram",
            "facebook",
            "linkedin",
            "duty",
            "email",
            "fax",
            "image_url",
        ]


class KafedraStaffSerializer(StaffSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True, size_divider=1)

    class Meta:
        model = ministry.Staff
        fields = ["id", "image_url", "title", "email", "position"]


class StudyProgramListSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.StudyProgram
        fields = ("id", "title", "description", "image_url", "views", "link")


class TopStudyProgramListSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.StudyProgram
        fields = ("id", "title", "image_url", "link")


class StudyProgramDetailSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.StudyProgram
        fields = (
            "id",
            "title",
            "description",
            "image_url",
            "views",
            "bachelor",
            "bachelor_documents",
            "master",
            "content",
            "publish_date",
            "link",
        )


class NightProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.NightProgram
        fields = (
            "id",
            "title",
            "address",
            "phone_number",
            "email",
            "fax",
            "content",
            "goals_tasks",
            "tasks",
            "bachelor",
            "directions",
        )


class KafedraListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Kafedra
        fields = ("id", "title", "about", "slug")


class KafedraFacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Department
        fields = ("id", "title", "slug")


class KafedraDetailSerializer(serializers.ModelSerializer):
    staffs = KafedraStaffSerializer(many=True)
    mudir = StaffListSerializer()

    class Meta:
        model = ministry.Kafedra
        fields = ("id", "title", "mudir", "about", "staffs", "faculty", "content", "slug")


class OrganizationDetailSerializer(serializers.ModelSerializer):
    staffs = StaffListSerializer(many=True)
    reg_image_url = ThumbnailImageSerializer(source="reg_image", read_only=True)

    class Meta:
        model = ministry.Organization
        fields = ("id", "title", "staffs", "content", "slug", "reg_link", "reg_title", "reg_subtitle", "reg_image_url")


class OrganizationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Organization
        fields = ("id", "title", "slug")


class CouncilStaffListSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True, size_divider=2, quality=90)

    class Meta:
        model = ministry.CouncilStaff
        fields = ("id", "image_url", "title", "shifr", "about")


class CouncilListSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.Council
        fields = (
            "id",
            "image_url",
            "title",
            "content",
        )


class CampImageSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "src": value.url,
        }
        return obj


# class CampSerilizer(serializers.ModelSerializer):
#     images = CampImageSerializer(read_only=True, many=True)
#
#     class Meta:
#         model = ministry.Camp
#         fields = ('id', 'images', 'content', 'long', 'lat')


class StatisticSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.Statistic
        fields = ("title", "icon_url", "blue_icon_url", "content", "why_tsue", "image_url", "link")


class StatisticItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.StatisticItem
        fields = ("id", "title", "number", "icon_url", "blue_icon_url", "order")


class StatisticContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ministry.StatisticContentItem
        fields = ("id", "content", "order")


class AnnouncementSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Announcement
        fields = ("id", "title", "content", "link")


class FamousGraduateMainSerailizer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.FamousGraduate
        fields = ("id", "title", "profession", "image_url", "quote", "slug", "order")


class FamousGraduateListSerailizer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.FamousGraduate
        fields = ("id", "title", "profession", "faculty", "year", "image_url", "slug", "order")


class FamousGraduateDetailSerailizer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.FamousGraduate
        fields = ("id", "title", "profession", "faculty", "year", "image_url", "bio", "tasks", "slug")


class FamousGraduateGallerySerailizer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ministry.FamousGraduateGallery
        fields = ("id", "image_url")


class UstavSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ministry.Ustav
        fields = ("title", "sub_title", "short_description")


class FAQQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.FAQQuestion
        fields = ("title", "content", "created_at")