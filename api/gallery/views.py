from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from api import pagination

from admin_panel.model import press_service


class PhotoListView(viewsets.ModelViewSet):
    queryset = press_service.PhotoGallery.objects.filter(is_published=True).order_by("-publish_date")
    serializer_class = serializers.PhotoSerializer
    pagination_class = pagination.Middle
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.PhotoDetailSerializer
        return serializers.PhotoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # instance.views += 1
        # instance.save()
        related = self.queryset.exclude(id=instance.id)[:4]
        related_serializer = serializers.PhotoSerializer

        payload = {"news": self.get_serializer(instance).data, "related": related_serializer(related, many=True).data}
        return Response(payload)


class VideoListView(viewsets.ModelViewSet):
    queryset = press_service.VideoGallery.objects.filter(is_published=True).order_by("-publish_date")
    serializer_class = serializers.VideoSerializer
    pagination_class = pagination.MidShort
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.VideoDetailSerializer
        return serializers.VideoSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        payload = {
            "single": self.get_serializer(instance).data,
            "related": serializers.VideoSerializer(self.get_queryset().exclude(pk=instance.pk)[:4], many=True).data,
        }
        return Response(payload)


class VebinarListView(viewsets.ModelViewSet):
    queryset = press_service.Vebinar.objects.filter(is_published=True).order_by("-publish_date")
    serializer_class = serializers.VebinarSerializer
    pagination_class = pagination.MidShort
    http_method_names = ["get"]


class TopVebinarView(viewsets.ModelViewSet):
    queryset = press_service.Vebinar.objects.filter(is_published=True, main_page=True).order_by("-publish_date")
    serializer_class = serializers.VebinarSerializer
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        instance = self.queryset[:4]
        # vebinar = self.queryset.first()
        # top = []
        # if vebinar:
        #     instance = self.queryset.exclude(id=vebinar.id)[:4]
        #     top.append(serializer(vebinar).data)
        #
        # payload = {
        #     'top': top,
        #     'vebinars': serializer(instance, many=True).data
        # }
        # return Response(payload)
        return Response(serializer(instance, many=True).data)


# class TopVideoView(viewsets.ModelViewSet):
#     queryset = press_service.VideoGallery.objects.filter(is_published=True, main_page=True).order_by(
#         '-publish_date')
#     serializer_class = serializers.VideoSerializer
#     pagination_class = None
#     http_method_names = ['get']
#
#     def list(self, request, *args, **kwargs):
#         serializer = self.serializer_class
#         instance = self.queryset[:5]
#         video = self.queryset.first()
#         top = []
#         if video:
#             instance = self.queryset.exclude(id=video.id)[:5]
#             top.append(serializer(video).data)
#
#
#
#         payload = {
#             'top': top,
#
#             'videos': serializer(instance, many=True).data
#         }
#         return Response(payload)

# class TopPhotoView(viewsets.ModelViewSet):
#     queryset = press_service.PhotoGallery.objects.filter(is_published=True, main_page=True).order_by(
#         '-publish_date')
#     serializer_class = serializers.PhotoSerializer
#     pagination_class = None
#     http_method_names = ['get']
#
#     def list(self, request, *args, **kwargs):
#         serializer = self.serializer_class
#         instance = self.queryset[:10]
#         photo = self.queryset.first()
#         if not photo:
#             top = {}
#         else:
#             instance = self.queryset[:10]
#             top = serializer(photo).data
#
#         payload = {
#             'photos': serializer(instance, many=True).data
#         }
#         return Response(payload)
