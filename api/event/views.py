from rest_framework import viewsets, generics
from rest_framework.response import Response

from admin_panel.model import event
from . import serializers
from api import pagination
from .filters import EventFilter


class EventListView(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = event.Event.objects.filter(is_published=True).order_by("-start_time")
    serializer_class = serializers.EventSerializer
    pagination_class = pagination.Middle
    http_method_names = ["get"]
    filter_class = EventFilter

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.EventDetailSerializer
        return serializers.EventSerializer

    def get_queryset(self):
        return self.queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TopEventView(EventListView):
    queryset = event.Event.objects.filter(is_published=True, main_page=True).order_by("-start_time")

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset()[:3]
        serializer = self.get_serializer_class()
        return Response(serializer(instance, many=True).data)
