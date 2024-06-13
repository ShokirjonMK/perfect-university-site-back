from rest_framework import serializers

from syllabus.models import CourseLesson


class CourseLessonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ["id"]
