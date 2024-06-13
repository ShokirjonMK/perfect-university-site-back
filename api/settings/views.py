from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from admin_panel.model import settings, territorial, ministry
from admin_panel.model import menu
from admin_panel.model import useful_link
from django.db.models import Q

from ..serializers import RegionSerializer


class SiteContactView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.HeaderSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.last()
        serializer = self.get_serializer(instance).data
        return Response(serializer)


class RekvizitView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.RekvizitSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.last()
        serializer = self.get_serializer(instance).data
        return Response(serializer)


class HeaderView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.HeaderSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.last()
        obj = menu.Menu.objects.filter(parent__isnull=True, only_footer=False, is_active=True)
        serializer = self.serializer_class
        object_serializer = serializers.MenuSerializer
        # main_service = service.Service.objects.filter(main_page=True)[:6]
        # main_service = ServiceSerializer(main_service, many=True)
        top_links = settings.TopLink.objects.all()
        payload = {
            "site": serializer(instance).data,
            # 'service': main_service.data,
            "menu": object_serializer(obj, many=True).data,
            "top_links": serializers.TopLinkSerializer(top_links, many=True).data,
        }
        return Response(payload)


class FooterView(viewsets.ModelViewSet):
    queryset = settings.MainPageSetting.objects.all()
    serializer_class = serializers.FooterSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.last()
        obj = menu.Menu.objects.filter(Q(footer=True) | Q(only_footer=True), parent__isnull=True).distinct()
        serializer = self.get_serializer_class()
        object_serializer = serializers.FooterMenuSerializer
        payload = {
            "footer": serializer(instance).data,
            "menu": object_serializer(obj, many=True).data,
        }
        return Response(payload)


class PartnersView(viewsets.ModelViewSet):
    queryset = useful_link.UsefulLink.objects.all()
    serializer_class = serializers.PartnerSerializer
    pagination_class = None
    http_method_names = ["get"]


class RegionView(viewsets.ModelViewSet):
    queryset = territorial.Region.objects.all()
    serializer_class = RegionSerializer
    pagination_class = None
    http_method_names = ["get"]


class RegionalDepartmentView(viewsets.ModelViewSet):
    queryset = ministry.RegionalDepartment.objects.all()
    serializer_class = serializers.RegionalDepartmentSerializer
    pagination_class = None
    http_method_names = ["get"]


class SliderView(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = settings.Slider.objects.all()[:4]
    serializer_class = serializers.SliderSerializer


class ImageUploadView(generics.CreateAPIView):
    queryset = settings.MediaImage.objects.all()
    serializer_class = serializers.MediaImageSerializer
    permission_classes = [IsAuthenticated]


class SidebarViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = settings.Sidebar.objects.all()
    serializer_class = serializers.SidebarSerializer


class MainPageDataView(generics.RetrieveAPIView):
    serializer_class = serializers.MainPageDataSerializer
    http_method_names = ["get"]

    def get_object(self):
        return settings.MainPageData.objects.last()


class EntrantPageQuestionView(generics.ListAPIView):
    pass
