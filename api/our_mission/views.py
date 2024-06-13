from rest_framework import generics

from admin_panel.model.static import OurMission
from api.our_mission.serializers import OurMissionModelSerializer


class OurMissionListAPIView(generics.ListAPIView):
    queryset = OurMission.objects.all()
    serializer_class = OurMissionModelSerializer
    filterset_fields = ("is_main",)


__all__ = ["OurMissionListAPIView"]
