from rest_framework import serializers

from syllabus.models import CourseLessonResource, CourseLessonResourceSingleFile


class CourseLessonResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonResource
        fields = [
            "id",
            "updated_at",
            "course_lesson",
            "course_syllabus",
            "type",
            "title",
            "file_name",
            "file",
            "url",
            "file_size",
            "order",
        ]


class CourseLessonResourceSingleFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLessonResourceSingleFile
        fields = [
            "id",
            "file",
        ]


class CourseLessonResourceFileSerializer(CourseLessonResourceSerializer):
    files = CourseLessonResourceSingleFileSerializer(many=True, read_only=True)

    class Meta:
        model = CourseLessonResource
        fields = [
            "id",
            "updated_at",
            "course_lesson",
            "course_syllabus",
            "type",
            "title",
            "file_name",
            "file",
            "files",
            "url",
            "file_size",
            "order",
        ]
