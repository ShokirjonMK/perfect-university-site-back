from rest_framework.generics import RetrieveAPIView

from .serializers import TestAnswerDetailSerializer
from syllabus.models import TestAnswer


class CheckTestAnswerView(RetrieveAPIView):
    serializer_class = TestAnswerDetailSerializer

    def get_queryset(self):
        return TestAnswer.objects.all()


__all__ = ["CheckTestAnswerView"]
