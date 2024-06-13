from rest_framework import viewsets
from rest_framework.response import Response

from admin_panel.model import service
from . import serializers


class ServiceTopListView(viewsets.ModelViewSet):
    queryset = service.Service.objects.filter(main_page=True)
    serializer_class = serializers.ServiceTopSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()[:6]
        serializer = self.serializer_class
        return Response(serializer(instance, many=True).data)


class ServiceListView(viewsets.ModelViewSet):
    queryset = service.Service.objects.filter(main_page=True)
    serializer_class = serializers.ServiceSerializer
    pagination_class = None
    http_method_names = ["get"]
