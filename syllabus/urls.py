from django.urls import path

from .api_endpoints.course_lesson import CourseLessonDetailView, CourseLessonListView
from .api_endpoints.course_resource import (
    CourseLessonResourceFileListView,
    CourseLessonResourceUrlListView,
    CourseLessonResourceVideoListView,
    CourseLessonResourceLectureListView,
)
from .api_endpoints.course_syllabus import (
    CourseSyllabusListView,
    CourseSyllabusDetailView,
    ProcedureAssessmentListView,
    CourseSyllabusSlugDetailView,
)
from .api_endpoints.syllabus import SyllabusListView, SyllabusDetailView, SyllabusSlugDetailView
from .api_endpoints.syllabus_test import SyllabusTestListAPIView, SyllabusTestSlugListAPIView
from .api_endpoints.syllabus_test import TestQuestionListAPIView, CheckTestAnswerView

app_name = "syllabus"

urlpatterns = [
    path(
        "course_resource/CourseResourceLessonFile/",
        CourseLessonResourceFileListView.as_view(),
        name="CourseResourceLessonFileList",
    ),
    path(
        "course_resource/CourseResourceLessonUrl/",
        CourseLessonResourceUrlListView.as_view(),
        name="CourseResourceLessonUrlList",
    ),
    path(
        "course_resource/CourseResourceLessonVideo/",
        CourseLessonResourceVideoListView.as_view(),
        name="CourseResourceLessonVideoList",
    ),
    path(
        "course_resource/CourseResourceLessonLecture/",
        CourseLessonResourceLectureListView.as_view(),
        name="CourseResourceLessonLectureList",
    ),
    path("course_lesson/CourseLessonDetail/<int:pk>/", CourseLessonDetailView.as_view(), name="CourseLessonDetail"),
    path("course_lesson/CourseLessonList/", CourseLessonListView.as_view(), name="CourseLessonList"),
    path("course_syllabus/SyllabusList/", CourseSyllabusListView.as_view(), name="CourseSyllabusList"),
    path("course_syllabus/SyllabusDetail/<int:pk>", CourseSyllabusDetailView.as_view(), name="CourseSyllabusDetail"),
    path(
        "course_syllabus/SyllabusDetail/<str:slug>",
        CourseSyllabusSlugDetailView.as_view(),
        name="CourseSyllabusSlugDetail",
    ),
    path("syllabus/DepartmentSyllabusList/", SyllabusListView.as_view(), name="SyllabusList"),
    path("syllabus/DepartmentSyllabusDetail/<int:pk>", SyllabusDetailView.as_view(), name="SyllabusDetail"),
    path(
        "syllabus/DepartmentSyllabusSlugDetailView/<str:slug>",
        SyllabusSlugDetailView.as_view(),
        name="SyllabusDetailSlug",
    ),
    path("syllabus/ProcedureAssessmentList/", ProcedureAssessmentListView.as_view(), name="ProcedureAssessmentList"),
    path("test/SyllabusTestList/<int:syllabus_id>/", SyllabusTestListAPIView.as_view(), name="SyllabusTestList"),
    path(
        "test/SyllabusTestList/<str:syllabus_slug>/", SyllabusTestSlugListAPIView.as_view(), name="SyllabusTestSlugList"
    ),
    path("test/TestQuestionList/<int:test_id>/", TestQuestionListAPIView.as_view(), name="TestQuestionList"),
    path("test/CheckTestAnswer/<int:pk>/", CheckTestAnswerView.as_view(), name="CheckTestAnswer"),
]
