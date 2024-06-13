from django.contrib.auth.models import User
from rest_framework import serializers
from django.db.models.functions import Coalesce
from django.db.models import Sum

from admin_panel.model.ministry import Department
from api.serializers import ThumbnailImageSerializer
from syllabus import models as syllabus_models
from admin_panel.model.courses import Direction
from syllabus.api_endpoints.course_syllabus.ProcedureAssessment.serializer import StudentAssessmentSerializer


class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = ["id", "title"]
        ref_name = "CourseSyllabusDetailSerializer_DirectionSerializer"


class CourseSyllabusTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = syllabus_models.CourseSyllabusTest
        fields = [
            "id",
            "title",
        ]
        ref_name = "CourseSyllabusDetailSerializer_CourseSyllabusTestSerializer"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
        ref_name = "CourseSyllabusRetrieveTeacher"


class CourseSyllabusInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = syllabus_models.CourseSyllabusInformation
        fields = ["id", "type", "text"]
        ref_name = "CourseSyllabusInformationSerializer"


class CourseSyllabusTextSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = syllabus_models.CourseSyllabusTextSection
        fields = ["id", "title", "type", "text"]
        ref_name = "CourseSyllabusTextSectionSerializer"


class DepartmentSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = Department
        fields = ("id", "title", "image_url", "slug", "main_page", "description")
        ref_name = "SyllabusDepartmentSerializer"


class SyllabusLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = syllabus_models.SyllabusLanguage
        fields = ("id", "name", "language_code")
        ref_name = "CourseSyllabusDetail_SyllabusLanguageSerializer"


class SyllabusSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()

    class Meta:
        model = syllabus_models.Syllabus
        fields = ("id", "department")
        ref_name = "CourseSyllabusDetail_SyllabusSerializer"


class CourseSyllabusDetailSerializer(serializers.ModelSerializer):
    teacher = UserSerializer()

    direction = DirectionSerializer()

    syllabus = SyllabusSerializer()
    language = SyllabusLanguageSerializer()

    course_syllabus_text_sections = CourseSyllabusTextSectionSerializer(many=True)
    course_syllabus_informations = CourseSyllabusInformationSerializer(many=True)

    test = CourseSyllabusTestSerializer(source="course_syllabus_test")

    total_stats = serializers.SerializerMethodField()
    student_assessments = StudentAssessmentSerializer(many=True)

    class Meta:
        model = syllabus_models.CourseSyllabus
        fields = [
            "id",
            "title",
            "direction",
            "teacher",
            "language",
            "year",
            "syllabus",
            "course_syllabus_text_sections",
            "course_syllabus_informations",
            "test",
            "total_stats",
            "student_assessments"
        ]

    def get_total_stats(self, obj):
        courses = obj.course_lessons.all()
        types = syllabus_models.CourseLessonHour.TypeTextChoices

        total_lecture = 0
        total_practical_training = 0
        total_laboratory_training = 0
        total_exams = 0
        total_independent_edu = 0
        total = 0

        for course in courses:
            hours = course.course_lesson_hours.all()
            total_lecture += hours.filter(type=types.lecture).aggregate(total=Coalesce(Sum('hour'), 0))['total']
            total_practical_training += hours.filter(type=types.practice).aggregate(total=Coalesce(Sum('hour'), 0))[
                'total']
            total_laboratory_training += hours.filter(type=types.laboratory).aggregate(total=Coalesce(Sum('hour'), 0))[
                'total']
            total_exams += hours.filter(type=types.exam).aggregate(total=Coalesce(Sum('hour'), 0))['total']
            total_independent_edu += \
                hours.filter(type=types.independent_education).aggregate(total=Coalesce(Sum('hour'), 0))['total']

        total += total_lecture + total_practical_training + total_laboratory_training + total_exams + total_independent_edu

        data = {
            "total_lecture": total_lecture,
            "total_practical_training": total_practical_training,
            "total_laboratory": total_laboratory_training,
            "total_exam": total_exams,
            "total_independent": total_independent_edu,
            "total": total

        }

        return data
