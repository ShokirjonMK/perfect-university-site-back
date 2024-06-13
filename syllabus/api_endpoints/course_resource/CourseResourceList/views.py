from rest_framework.generics import ListAPIView

from syllabus.models import (
    CourseLessonResourceLecture,
    CourseLessonResourceVideo,
    CourseLessonResourceFile,
    CourseLessonResourceUrl,
    CourseLessonResource,
)
from .filters import CourseLessonResourceFilterSet
from .serializers import CourseLessonResourceSerializer, CourseLessonResourceFileSerializer


class CourseLessonResourceListView(ListAPIView):
    serializer_class = CourseLessonResourceSerializer
    model_class = CourseLessonResource
    filterset_class = CourseLessonResourceFilterSet

    def get_queryset(self):
        return self.model_class.objects.filter_by_type()


class CourseLessonResourceLectureListView(CourseLessonResourceListView):
    model_class = CourseLessonResourceLecture


class CourseLessonResourceVideoListView(CourseLessonResourceListView):
    model_class = CourseLessonResourceVideo


class CourseLessonResourceFileListView(CourseLessonResourceListView):
    model_class = CourseLessonResourceFile
    serializer_class = CourseLessonResourceFileSerializer


class CourseLessonResourceUrlListView(CourseLessonResourceListView):
    model_class = CourseLessonResourceUrl


__all__ = [
    "CourseLessonResourceLectureListView",
    "CourseLessonResourceVideoListView",
    "CourseLessonResourceFileListView",
    "CourseLessonResourceUrlListView",
]
