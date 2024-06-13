from rest_framework.generics import RetrieveAPIView
from syllabus.models import CourseSyllabus
from .serializers import CourseSyllabusDetailSerializer


class CourseSyllabusDetailView(RetrieveAPIView):
    serializer_class = CourseSyllabusDetailSerializer

    def get_queryset(self):
        qs = CourseSyllabus.objects.prefetch_related("course_syllabus_text_sections", "course_syllabus_informations")
        qs.select_related("teacher")
        return qs


class CourseSyllabusSlugDetailView(CourseSyllabusDetailView):
    lookup_field = "slug"
    lookup_url_kwarg = "slug"

    def get_queryset(self):
        qs = CourseSyllabus.objects.prefetch_related("course_syllabus_text_sections", "course_syllabus_informations")
        qs.select_related("teacher")
        return qs
