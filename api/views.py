from sentry_sdk import capture_exception

from admin_panel.model import territorial
from admin_panel.model import menu
from rest_framework import generics
from django.utils.translation import gettext_lazy as _

from . import serializers
from rest_framework.response import Response
from rest_framework import status


class MyListAPIView(generics.ListAPIView):
    def get(self, request, pk=None, format=None):
        if pk is None:
            response = super().list(request)
            return response
        try:
            obj = self.get_object()
        except self.queryset.model.DoesNotExist:
            return Response(
                {"status": "error", "Message": _("Mavjud emas"), "data": {}}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(obj)
        return Response(serializer.data)


# REGION
class RegionListView(MyListAPIView):
    queryset = territorial.Region.objects.all()
    serializer_class = serializers.RegionSerializer
    pagination_class = None


# MENU
class MenuRetrieveView(MyListAPIView):
    http_method_names = ["get"]
    queryset = menu.Menu.objects.all()
    serializer_class = serializers.MenuSerializer

    def get(self, request, slug=None, format=None):
        serializer = self.serializer_class
        try:
            child = self.queryset.get(parent__isnull=False, slug=slug)
            parent_menu = child.parent

        except Exception as ex:
            capture_exception(ex)
            parent_menu = self.queryset.filter(parent__isnull=True).first()

        return Response(serializer(parent_menu).data, status=status.HTTP_200_OK)
