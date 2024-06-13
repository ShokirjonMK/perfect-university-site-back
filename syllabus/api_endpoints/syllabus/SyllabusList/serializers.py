from rest_framework import serializers

from admin_panel.model.ministry import Department
from syllabus.models import Syllabus


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "title", "image", "slug", "main_page", "description")
        ref_name = "SyllabusDepartmentSerializer"


class SyllabusSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = Syllabus
        fields = ("id", "title", "department")
