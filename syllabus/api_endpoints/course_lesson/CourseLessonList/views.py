from rest_framework.generics import ListAPIView

from syllabus.models import CourseLesson
from .filters import CourseLessonFilterSet
from .serializers import CourseLessonSerializer


class CourseLessonListView(ListAPIView):
    serializer_class = CourseLessonSerializer
    filterset_class = CourseLessonFilterSet

    def get_queryset(self):
        return CourseLesson.objects.prefetch_related("course_lesson_hours")
