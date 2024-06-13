from rest_framework.generics import ListAPIView

from .serializer import StudentAssessmentSerializer
from syllabus.models import StudentAssessment


class ProcedureAssessmentListView(ListAPIView):
    serializer_class = StudentAssessmentSerializer

    def get_queryset(self):
        return StudentAssessment.objects.order_by("order")


__all__ = ["ProcedureAssessmentListView"]
