from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from api import pagination
from . import serializers

from admin_panel.model import activity
from hr.models import Job, JobCategory


# Articles
class ArticlesListView(viewsets.ModelViewSet):
    queryset = activity.Articles.objects.all()
    serializer_class = serializers.ArticlesSerializer
    pagination_class = pagination.Middle
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ArticlesDetailSerializer
        return serializers.ArticlesSerializer


# Opendata
class OpendataListView(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = activity.Opendata.objects.all()
    serializer_class = serializers.OpendataSerializer
    pagination_class = pagination.Middle
    # http_method_names = ['get']
    # filter_backends = [DjangoFilterBackend]

    # def get_serializer_class(self):
    #     if self.action == 'retrieve':
    #         return serializers.OpendataDetailSerializer
    #     return serializers.OpendataSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     instance.views += 1
    #     instance.save()
    #     serializer = self.get_serializer_class()
    #     list_serializer = serializers.OpendataSerializer
    #     related = self.queryset.exclude(id=instance.id)[:4]
    #     payload = {
    #         'opendata': serializer(instance).data,
    #         'related': list_serializer(related, many=True).data
    #     }
    #
    #     return Response(payload, status=200)


# class IndexOpendataListView(viewsets.ModelViewSet):
#     queryset = activity.Opendata.objects.all()
#     serializer_class = serializers.IndexOpendataDetailSerializer
#     pagination_class = pagination.Middle
#     http_method_names = ['get']
#     filter_backends = [DjangoFilterBackend]
#
#     def list(self, request, *args, **kwargs):
#         serializer = serializers.IndexOpendataDetailSerializer
#         year = self.request.GET.get('year')
#
#         if year:
#             opendata = activity.Opendata.objects.filter(
#                 publish_date__year=year)
#         else:
#             opendata = activity.Opendata.objects.all()
#
#         instance = opendata[:5]
#         return Response(serializer(instance, many=True).data, status=200)
#
#     # Thesis


class JobListView(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    pagination_class = pagination.Per20
    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.JobDetailSerializer
        return serializers.JobSerializer

    def retrieve(self, request, *args, **kwargs):
        # customization here
        instance = self.get_object()
        instance.views += 1
        instance.save()
        return Response(self.get_serializer(instance).data)


class JobCategoryList(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = serializers.JobCategorySerializer
    http_method_names = ["get"]
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class StudentActivityCategoryListAPIView(generics.ListAPIView):
    queryset = activity.StudentActivityCategory.objects.all()
    serializer_class = serializers.StudentActivityCategorySerializer
    filter_backends = [SearchFilter]
    filterset_fields = ['slug']
    search_fields = ["title"]


class StudentActivitiesListAPIView(generics.ListAPIView):
    queryset = activity.StudentActivities.objects.all().select_related("category").prefetch_related("images")
    serializer_class = serializers.StudentActivitiesListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__slug"]


class StudentActivityRetreviewAPIView(generics.RetrieveAPIView):
    queryset = activity.StudentActivities.objects.all()
    serializer_class = serializers.StudentActivitiesSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        activity = self.get_object()
        activity.views += 1
        activity.save()
        serializer = self.get_serializer(activity)

        return Response(serializer.data)


class AcademicCalendarListAPIView(generics.ListAPIView):
    queryset = activity.AcademicCalendar.objects.all().prefetch_related("files")
    serializer_class = serializers.AcademicCalendarSerializer
    filter_backends = [SearchFilter]
    search_fields = ["title"]


class StudentVideoListAPIView(generics.ListAPIView):
    queryset = activity.StudentVideo.objects.all().order_by("-created_at")
    serializer_class = serializers.StudentVideoSerializers
    filter_backends = [SearchFilter]
    search_fields = ["title"]
