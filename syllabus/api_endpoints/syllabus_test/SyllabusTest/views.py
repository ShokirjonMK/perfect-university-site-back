from rest_framework.generics import ListAPIView

from syllabus.models import CourseSyllabusTest
from .serializers import CourseSyllabusTestListSerializer


class SyllabusTestListAPIView(ListAPIView):
    serializer_class = CourseSyllabusTestListSerializer
    queryset = CourseSyllabusTest.objects.all()

    def get_queryset(self):
        syllabus_id = self.kwargs.get("syllabus_id")
        return CourseSyllabusTest.objects.filter(
            course_syllabus_id=syllabus_id,
        )


class SyllabusTestSlugListAPIView(SyllabusTestListAPIView):
    def get_queryset(self):
        syllabus_slug = self.kwargs.get("syllabus_slug")
        return CourseSyllabusTest.objects.filter(
            course_syllabus__slug=syllabus_slug,
        )
