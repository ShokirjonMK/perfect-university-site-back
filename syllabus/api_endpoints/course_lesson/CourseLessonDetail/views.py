from rest_framework.generics import RetrieveAPIView

from syllabus.models import CourseLesson
from .serializers import CourseLessonDetailSerializer


class CourseLessonDetailView(RetrieveAPIView):
    serializer_class = CourseLessonDetailSerializer

    def get_queryset(self):
        return CourseLesson.objects.all()
