from syllabus.models import CourseSyllabusTest
from rest_framework import serializers


class CourseSyllabusTestListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSyllabusTest
        fields = [
            "id",
            "course_syllabus",
        ]
