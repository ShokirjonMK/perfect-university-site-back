from rest_framework import viewsets, generics
from rest_framework.response import Response

from admin_panel.model import courses
from api import pagination
from . import serializers


class CourseCatalogViewSet(viewsets.ModelViewSet):
    """
    'is_admission':true or false on retrieve response
    """

    queryset = courses.CourseCatalog.objects.all()
    serializer_class = serializers.CourseCatalogSerializer
    lookup_field = "slug"
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.CourseCatalogDetailSerializer
        return serializers.CourseCatalogSerializer

    def get_queryset(self):
        if self.action == "retrieve":
            return self.queryset.filter(directions__is_admission=True)
        return self.queryset


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = courses.Direction.objects.all()
    serializer_class = serializers.DirectionListSerializer
    http_method_names = ["get"]
    pagination_class = pagination.Per20
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DirectionDetailSerializer
        return serializers.DirectionListSerializer

    def get_queryset(self):
        return self.queryset.filter(course__slug=self.kwargs.get("course_slug"))

    def list(self, request, *args, **kwargs):
        response = super(DirectionViewSet, self).list(request, args, kwargs)
        # Add data to response.data Example for your object:
        response.data["title"] = courses.CourseCatalog.objects.get(
            slug=self.kwargs.get("course_slug")
        ).title  # Or wherever you get this values from
        return response


class RatingSystemViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = courses.RatingSystem.objects.all()
    serializer_class = serializers.RatingSystemSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        queryset = self.get_queryset()
        courses = queryset.values_list("direction__course__pk", "direction__course__title").distinct(
            "direction__course"
        )
        payload_data = []
        for course in courses:
            payload_data.append(
                {
                    "course": {
                        "title": course[1],
                        "ratingSystems": serializer(queryset.filter(direction__course__pk=course[0]), many=True).data,
                    }
                }
            )
        return Response(payload_data)


class QualificationRequirementsViewSet(viewsets.ModelViewSet):
    queryset = courses.QualificationRequirement.objects.all()
    serializer_class = serializers.QualificationRequirementsSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        queryset = self.get_queryset()
        courses = queryset.values_list("direction__course__pk", "direction__course__title").distinct(
            "direction__course"
        )
        payload_data = []
        for course in courses:
            payload_data.append(
                {
                    "course": {
                        "title": course[1],
                        "ratingSystems": serializer(queryset.filter(direction__course__pk=course[0]), many=True).data,
                    }
                }
            )
        return Response(payload_data)


class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = courses.Curriculum.objects.all()
    serializer_class = serializers.CurriculumSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class
        queryset = self.get_queryset()
        courses = queryset.values_list("direction__course__pk", "direction__course__title").distinct(
            "direction__course"
        )
        payload_data = []
        for course in courses:
            payload_data.append(
                {
                    "course": {
                        "title": course[1],
                        "ratingSystems": serializer(queryset.filter(direction__course__pk=course[0]), many=True).data,
                    }
                }
            )
        return Response(payload_data)


class EntrantPage(viewsets.ReadOnlyModelViewSet):
    """
    'is_admission':true or false on retrieve response
    """

    queryset = courses.EntrantPage.objects.all()
    serializer_class = serializers.EntrantPageListSerializer
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.EntrantPageDetailSerializer
        return serializers.EntrantPageListSerializer


class AdmissionPageView(viewsets.GenericViewSet, generics.CreateAPIView):
    """
    'is_admission':true or false
    """

    serializer_class = serializers.AdmissionPageDetailSerializer

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset()).data)

    def get_queryset(self):
        if courses.AdmissionPage.objects.last():
            return courses.AdmissionPage.objects.last()
        else:
            return courses.AdmissionPage.objects.create()
