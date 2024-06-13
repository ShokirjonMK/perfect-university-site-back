from django.contrib.auth.models import User
from rest_framework import serializers

import syllabus.models as syllabus_models
from admin_panel.model.ministry import Department
from admin_panel.model.user import CustomUser
from api.serializers import ThumbnailImageSerializer
from admin_panel.model.courses import Direction


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ["id", "title"]
        ref_name = "CourseSyllabusListSerializer_DirectionSerializer"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
        ref_name = "CourseSyllabusListTeacher"


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "user",
            "email",
            "phone",
            "image",
            "created_at",
            "updated_at",
        )
        ref_name = "CourseSyllabusListTeacher"


class DepartmentSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = Department
        fields = ("id", "title", "image_url", "slug", "main_page", "description")
        ref_name = "CourseSyllabusDetail_DepartmentSerializer"


class SyllabusSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = syllabus_models.Syllabus
        fields = ("id", "title", "department")
        ref_name = "CourseSyllabusList_SyllabusSerializer"


class CourseSyllabusListSerializer(serializers.ModelSerializer):
    direction = DirectionSerializer()
    teacher = CustomUserSerializer()
    year = serializers.IntegerField(source="year.year")
    department_syllabus = SyllabusSerializer(source="syllabus")

    class Meta:
        model = syllabus_models.CourseSyllabus
        fields = ("id", "teacher", "title", "direction", "teacher", "language", "year", "department_syllabus")
