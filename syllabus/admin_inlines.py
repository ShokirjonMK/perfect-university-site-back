from django.contrib import admin

from . import models as syllabus_models
from .forms import TestAnswerAdminForm, TestAnswerFormSet, CourseSyllabusTextSectionForm, CourseLessonInlineForm


class CourseLessonResourceInline(admin.TabularInline):
    model = syllabus_models.CourseLessonResource
    extra = 0

    def get_queryset(self, request):
        return super().get_queryset(request).filter_by_type()

    def get_exclude(self, request, obj=None):
        return ["course_syllabus", "type"]

    def get_readonly_fields(self, request, obj=None):
        return ["file_name", "file_size"]


class CourseLessonResourceUrlInline(CourseLessonResourceInline):
    model = syllabus_models.CourseLessonResourceUrl

    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj)
        return exclude + ["file", "file_name", "file_size"]


class CourseLessonResourceFileInline(CourseLessonResourceInline):
    model = syllabus_models.CourseLessonResourceFile


class CourseLessonResourceVideoInline(CourseLessonResourceInline):
    model = syllabus_models.CourseLessonResourceVideo


class CourseLessonResourceLectureInline(CourseLessonResourceInline):
    model = syllabus_models.CourseLessonResourceLecture


class CourseSyllabusTextSectionInline(admin.TabularInline):
    model = syllabus_models.CourseSyllabusTextSection
    extra = 7
    form = CourseSyllabusTextSectionForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


class CourseSyllabusInformationInline(admin.TabularInline):
    model = syllabus_models.CourseSyllabusInformation
    extra = 3

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


class CourseLessonHourInline(admin.TabularInline):
    model = syllabus_models.CourseLessonHour
    extra = 3

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return self.extra


class CourseLessonInline(admin.StackedInline):
    model = syllabus_models.CourseLesson
    form = CourseLessonInlineForm
    extra = 3


class TestQuestionInline(admin.TabularInline):
    model = syllabus_models.TestQuestion
    extra = 3


class TestAnswerInline(admin.TabularInline):
    model = syllabus_models.TestAnswer
    formset = TestAnswerFormSet
    form = TestAnswerAdminForm

    def get_extra(self, request, obj=None, **kwargs):
        if obj:
            return 0
        return 3


class StudentAssessmentInline(admin.TabularInline):
    model = syllabus_models.StudentAssessment
    extra = 3


class CourseLessonResourceSingleFileInline(admin.TabularInline):
    model = syllabus_models.CourseLessonResourceSingleFile
    extra = 0
