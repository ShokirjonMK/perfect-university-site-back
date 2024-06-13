from rest_framework import serializers
from sentry_sdk import capture_exception

from admin_panel.model import activity
import os
from hr.models import Job, JobCategory


def filename_minus_extension(file):
    basename = os.path.basename(file.name)
    return basename


def file_extension(file):
    _, ext = os.path.splitext(file.name)
    try:
        return ext[1:]
    except Exception as e:
        capture_exception(e)
        return ext


class ArticlesFileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "url": value.file_url,
            "size": value.file.size,
            "name": filename_minus_extension(value.file),
        }
        return obj


# Articles
class ArticlesSerializer(serializers.ModelSerializer):
    files = ArticlesFileSerializer(many=True, read_only=True)

    class Meta:
        model = activity.Articles
        fields = ["id", "title", "author", "views", "created_at", "files"]


# Opendata


class OpendataFileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "url": value.file_url,
            "format": file_extension(value.file),
        }
        return obj


class OpendataSerializer(serializers.ModelSerializer):
    files = OpendataFileSerializer(many=True, read_only=True)

    class Meta:
        model = activity.Opendata
        fields = ["id", "title", "url", "files"]


class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = ["id", "name"]


# Jobs
class JobSerializer(serializers.ModelSerializer):
    category = JobCategorySerializer()

    class Meta:
        model = Job
        fields = ["id", "title", "department", "salary", "salary_to", "views", "date", "category"]


class JobDetailSerializer(JobSerializer):
    class Meta:
        model = Job
        fields = ["id", "title", "department", "content", "salary", "salary_to", "views", "date", "form", "category"]


class IndexOpendataDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.Opendata
        fields = [
            "id",
            "title",
            "views",
            "created_at",
        ]


# class OpendataDetailSerializer(serializers.ModelSerializer):
#     files = OpendataFileSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = activity.Opendata
#         fields = [
#             'id', 'title', 'content', 'views', 'created_at', 'files',
#         ]


class StudentActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.StudentActivityCategory
        fields = ("id", "title", 'slug')

class StudentActivityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.StudentActivityImage
        fields = ("id", "image")


class StudentActivityContentTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.StudentActivityContentTag
        fields = ("id", "tag")


class StudentActivityContentSerializer(serializers.ModelSerializer):
    tags = StudentActivityContentTagSerializer(many=True, read_only=True)
    class Meta:
        model = activity.StudentActivityContent
        fields = ("id", 'title', "content", 'tags')

class StudentActivitiesListSerializer(serializers.ModelSerializer):
    category = StudentActivityCategorySerializer()
    images = StudentActivityImageSerializer(many=True, read_only=True)

    class Meta:
        model = activity.StudentActivities
        fields = ("id", "title", "slug", "short_description", "category", 'contents', "images", "views", "created_at")

class StudentActivitiesSerializer(serializers.ModelSerializer):
    category = StudentActivityCategorySerializer()
    images = StudentActivityImageSerializer(many=True, read_only=True)
    contents = StudentActivityContentSerializer(many=True, read_only=True)

    class Meta:
        model = activity.StudentActivities
        fields = ("id", "title", "slug", "short_description", "images", "contents", "category", "views", "created_at")


class AcademicCalendarFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.AcademicCalendarFile
        fields = ("id", "file")

class AcademicCalendarSerializer(serializers.ModelSerializer):
    files = AcademicCalendarFileSerializer(many=True, read_only=True)

    class Meta:
        model = activity.AcademicCalendar
        fields = ("id", "title",'files')



class StudentVideoSerializers(serializers.ModelSerializer):
    class Meta:
        model = activity.StudentVideo
        fields = (
            "id",
            "title",
            'thumbnail',
            "video_url",
            "video",
            "created_at"
        )