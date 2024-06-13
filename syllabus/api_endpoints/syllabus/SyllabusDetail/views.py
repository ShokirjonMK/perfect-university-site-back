from rest_framework.generics import RetrieveAPIView

from syllabus.models import Syllabus
from .serializers import SyllabusDetailSerializer


class SyllabusDetailView(RetrieveAPIView):
    serializer_class = SyllabusDetailSerializer

    def get_queryset(self):
        return Syllabus.objects.select_related("department")


class SyllabusSlugDetailView(SyllabusDetailView):
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
