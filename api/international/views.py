from rest_framework import viewsets, generics, exceptions, parsers
from rest_framework.response import Response
from api.international import serializers
from api import pagination
from admin_panel.model import international


class InternationalViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = international.Grant.objects.filter(is_published=True)
    pagination_class = pagination.Middle
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.GrantDetailSerializer
        return serializers.GrantListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class InternationalConferencePageViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.InternationalConferencePageSerializer
    queryset = international.InternationalConferencePage.objects.all()
    pagination_class = pagination.Middle

    def list(self, request, *args, **kwargs):
        page = international.InternationalConferencePage.objects.all()
        serializer = self.get_serializer(page, many=True)
        return Response(serializer.data)


class InternationalRelationView(generics.ListAPIView, viewsets.GenericViewSet):
    queryset = international.InternationalRelation.objects.all()
    serializer_class = serializers.InternationalRelationSerializer

    def list(self, request, *args, **kwargs):
        relations = serializers.InternationalRelationSerializer(self.queryset, many=True)
        staffs = serializers.InternationalStaffSerializer(international.InternationalStaff.objects.all(), many=True)
        usufull_links = serializers.InternationalUsufulLinkSerializer(
            international.InternationalUsufulLink.objects.all(), many=True
        )

        payload = {"relations": relations.data, "staffs": staffs.data, "usufull_links": usufull_links.data}
        return Response(payload)


class InternationalPartnerPageView(generics.ListAPIView, viewsets.GenericViewSet):
    queryset = international.InternationalPartnerPage.objects.all()
    serializer_class = serializers.InternationalPartnerPageSerializer

    def list(self, request, *args, **kwargs):
        if not international.InternationalPartnerPage.objects.last():
            international.InternationalPartnerPage.objects.create()

        page = serializers.InternationalPartnerPageSerializer(
            international.InternationalPartnerPage.objects.last()
        ).data
        payload = {
            "page": page,
            "partners": serializers.InternationalPartnerSerializer(
                international.InternationalPartner.objects.all(), many=True
            ).data,
        }
        return Response(payload)


# Sirtqi bo'lim views
class ExternalSectionListView(generics.ListAPIView):
    queryset = international.ExternalSection.objects.all()
    serializer_class = serializers.ExternalSectionListSerializer


class ExternalSectionDetailView(generics.RetrieveAPIView):
    queryset = international.ExternalSection.objects.all()
    serializer_class = serializers.ExternalSectionDetailSerializer


class InternationalFacultyPageDetailAPIView(generics.GenericAPIView):
    queryset = international.InternationalFacultyPage.objects.all()
    serializer_class = serializers.InternationalFacultyPageDetailSerializer

    def get(self, request, *args, **kwargs):
        instance = self.queryset.first()
        if not instance:
            raise exceptions.NotFound()
        return Response(data=self.serializer_class(instance).data)


class InternationalFacultyApplicationCreateAPIView(generics.CreateAPIView):
    serializer_class = serializers.InternationalFacultyApplicationCreateSerializer
    queryset = international.InternationalFacultyApplication.objects.all()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
    )


class InternationalCooperationListAPIView(generics.ListAPIView):
    queryset = international.InternationalCooperation.objects.all()
    serializer_class = serializers.InternationalCooperationModelSerializer


class RankingListAPIView(generics.ListAPIView):
    queryset = international.Ranking.objects.all()
    pagination_class = None
    serializer_class = serializers.RankingModelSerializer


class JointProgramListAPIView(generics.ListAPIView):
    queryset = international.JointPrograms.objects.all()
    serializer_class = serializers.JointProgramsModelSerializer
