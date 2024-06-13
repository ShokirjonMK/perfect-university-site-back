import os

from django.utils.timezone import now
from rest_framework import serializers
from rest_framework.fields import MultipleChoiceField

from admin_panel.model import courses
from admin_panel.model.courses import EducationType


def filename(file):
    head, tail = os.path.split(file.name)
    return tail


class CourseCatalogSerializer(serializers.ModelSerializer):
    direction_count = serializers.IntegerField(source="directions.count")

    class Meta:
        model = courses.CourseCatalog
        fields = ("id", "title", "slug", "direction_count")


class CourseCatalogDirectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.Direction
        fields = ("id", "title", "shifr")


class CourseCatalogDetailSerializer(serializers.ModelSerializer):
    directions = CourseCatalogDirectionListSerializer(many=True, read_only=True)
    is_admission = serializers.SerializerMethodField()

    class Meta:
        model = courses.CourseCatalog
        fields = ("id", "title", "slug", "directions", "is_admission")

    def get_is_admission(self, obj):
        admission = courses.AdmissionPage.objects.last()
        today = now().date()
        if admission.start_date > today > admission.end_date:
            return True
        else:
            return False


class DirectionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.Direction
        fields = ("id", "title", "shifr", "slug")


class DirectionDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    education_type = MultipleChoiceField(choices=EducationType)

    class Meta:
        model = courses.Direction
        fields = (
            "id",
            "title",
            "shifr",
            "course",
            "languages",
            "qualification",
            "credits",
            "study_plan",
            "study_year",
            "content",
            "education_type",
            "slug",
        )

    def get_education_type(self, obj):
        return obj.get_education_type_display()


class RatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.RatingSystem
        fields = ("id", "title", "file_url")


class QualificationRequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.QualificationRequirement
        fields = ("id", "title", "file_url")


class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.Curriculum
        fields = ("id", "title", "file_url")


# EntrantPages
class EntrantPageFileSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "url": value.file_url,
            "filename": filename(value.file),
        }
        return obj


class EntrantPageQuestionSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "content": value.content,
        }
        return obj


class EntrantPageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = courses.EntrantPage
        fields = ("id", "title", "publish_date", "views", "slug")


class EntrantPageDetailSerializer(serializers.ModelSerializer):
    questions = EntrantPageQuestionSerializer(many=True, read_only=True)
    files = EntrantPageFileSerializer(many=True, read_only=True)
    is_admission = serializers.SerializerMethodField()

    class Meta:
        model = courses.EntrantPage
        fields = ("id", "title", "publish_date", "views", "files", "content", "questions", "slug", "is_admission")

    def get_is_admission(self, obj):
        admission = courses.AdmissionPage.objects.last()
        today = now().date()
        if admission.start_date > today > admission.end_date:
            return True
        else:
            return False


class AdmissionPageDetailSerializer(serializers.ModelSerializer):
    is_admission = serializers.SerializerMethodField()

    class Meta:
        model = courses.AdmissionPage
        fields = ("id", "title", "publish_date", "views", "content", "is_admission")

    def get_is_admission(self, obj):
        admission = courses.AdmissionPage.objects.last()
        today = now().date()
        if admission.start_date > today > admission.end_date:
            return True
        else:
            return False
