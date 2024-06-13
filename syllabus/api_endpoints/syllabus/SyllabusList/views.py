from rest_framework.generics import ListAPIView

from .serializers import SyllabusSerializer
from syllabus.models import Syllabus


class SyllabusListView(ListAPIView):
    serializer_class = SyllabusSerializer

    def get_queryset(self):
        return Syllabus.objects.select_related("department")
