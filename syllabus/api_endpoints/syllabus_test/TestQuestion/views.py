from django.db import models
from rest_framework.generics import ListAPIView

from .serializers import TestQuestionListSerializer
from syllabus.models import TestQuestion, TestAnswer


class TestQuestionListAPIView(ListAPIView):
    serializer_class = TestQuestionListSerializer

    def get_queryset(self):
        test_id = self.kwargs.get("test_id")
        test_answers_prefetch = models.Prefetch("test_answers", queryset=TestAnswer.objects.order_by("?"))
        return (
            TestQuestion.objects.select_related("test").filter(test__id=test_id).prefetch_related(test_answers_prefetch)
        )

    lookup_field = "test_id"


__all__ = ["TestQuestionListAPIView"]
