from rest_framework import generics
from .serializers import TeamListSerializer
from admin_panel.model import ministry


class TeamListApiView(generics.ListAPIView):
    serializer_class = TeamListSerializer
    queryset = ministry.Staff.objects.all()


class TeamMemberDetailApiView(generics.RetrieveAPIView):
    serializer_class = TeamListSerializer
    queryset = ministry.Staff.objects.all()
