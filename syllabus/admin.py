from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from . import admin_inlines
from . import models as syllabus_models
from .admin_inlines import CourseLessonResourceSingleFileInline
from .forms import TestQuestionAdminForm


@admin.register(syllabus_models.Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "get_department_title"]

    @admin.display(ordering="syllabus__title", description=_("Department"))
    def get_department_title(self, obj: syllabus_models.Syllabus):
        return obj.department.title

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("department")


@admin.register(syllabus_models.CourseSyllabus)
class CourseSyllabusAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "get_syllabus_title",
        "year",
    ]
    inlines = [
        admin_inlines.CourseSyllabusTextSectionInline,
        admin_inlines.CourseSyllabusInformationInline,
        admin_inlines.CourseLessonInline,
        admin_inlines.StudentAssessmentInline,
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("syllabus__department")

    @admin.display(ordering="syllabus__title", description=_("Department"))
    def get_syllabus_title(self, obj: syllabus_models.CourseSyllabus):
        return obj.syllabus.title


@admin.register(syllabus_models.SyllabusLanguage)
class SyllabusLanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(syllabus_models.CourseYear)
class CourseYearAdmin(admin.ModelAdmin):
    pass


class CourseLessonResourceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "course_syllabus", "type", "file_name", "file_size"]

    def get_queryset(self, request):
        return super().get_queryset(request).filter_by_type()

    def get_readonly_fields(self, request, obj=None):
        return ["file_size"]

    def get_exclude(self, request, obj=None):
        return [
            "type",
            "course_syllabus",
        ]


@admin.register(syllabus_models.CourseLessonResourceUrl)
class CourseLessonResourceUrlAdmin(CourseLessonResourceAdmin):
    def get_exclude(self, request, obj=None):
        return super().get_exclude(request, obj=obj) + [
            "file",
            "file_name",
        ]


@admin.register(syllabus_models.CourseLessonResourceFile)
class CourseLessonResourceFileAdmin(CourseLessonResourceAdmin):
    def get_exclude(self, request, obj=None):
        return super().get_exclude(request, obj=obj) + [
            "url",
        ]

    inlines = [
        CourseLessonResourceSingleFileInline,
    ]


@admin.register(syllabus_models.CourseLessonResourceLecture)
class CourseLessonResourceLectureAdmin(CourseLessonResourceAdmin):
    pass


@admin.register(syllabus_models.CourseLessonResourceVideo)
class CourseLessonResourceVideoAdmin(CourseLessonResourceAdmin):
    pass


@admin.register(syllabus_models.CourseSyllabusInformation)
class CourseSyllabusInformationAdmin(admin.ModelAdmin):
    list_display = ["id", "course_syllabus", "type"]
    list_filter = ["type", "course_syllabus"]


@admin.register(syllabus_models.CourseLessonHour)
class CourseLessonHourAdmin(admin.ModelAdmin):
    list_display = ["id", "lesson", "type", "hour"]
    list_filter = ["type", "lesson"]


@admin.register(syllabus_models.CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    list_display = ["title", "course_syllabus", "order"]

    inlines = [
        admin_inlines.CourseLessonHourInline,
        admin_inlines.CourseLessonResourceUrlInline,
        admin_inlines.CourseLessonResourceFileInline,
        admin_inlines.CourseLessonResourceVideoInline,
        admin_inlines.CourseLessonResourceLectureInline,
    ]

    def get_queryset(self, request):
        return (
            super().get_queryset(request).select_related("course_syllabus").prefetch_related("course_lesson_resource")
        )


@admin.register(syllabus_models.CourseSyllabusTest)
class CourseSyllabusTestAdmin(admin.ModelAdmin):
    inlines = [admin_inlines.TestQuestionInline]


@admin.register(syllabus_models.TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    inlines = [admin_inlines.TestAnswerInline]
    form = TestQuestionAdminForm

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        form.request = request
        return form


@admin.register(syllabus_models.StudentAssessment)
class StudentAssessmentAdmin(admin.ModelAdmin):
    list_display = ["id", "course_syllabus", "rating_assessment", "max_ball", "order"]
    list_filter = ["course_syllabus"]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("course_syllabus").order_by("order")
