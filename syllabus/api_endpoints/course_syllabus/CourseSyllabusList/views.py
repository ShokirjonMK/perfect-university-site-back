from rest_framework.generics import ListAPIView

from syllabus.models import CourseSyllabus
from .filters import CourseSyllabusFilterSet
from .serializers import CourseSyllabusListSerializer


class CourseSyllabusListView(ListAPIView):
    serializer_class = CourseSyllabusListSerializer
    filterset_class = CourseSyllabusFilterSet

    def get_queryset(self):
        return CourseSyllabus.objects.select_related("teacher__user")
