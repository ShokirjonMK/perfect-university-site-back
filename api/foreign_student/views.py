from rest_framework import generics

from admin_panel.model.ministry import ForeignStudent
from api.foreign_student.serializers import ForeignStudentModelSerializer


class ForeignStudentListAPIView(generics.ListAPIView):
    queryset = ForeignStudent.objects.all()
    serializer_class = ForeignStudentModelSerializer


__all__ = ["ForeignStudentListAPIView"]
