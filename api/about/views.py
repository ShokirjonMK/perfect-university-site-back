from rest_framework import viewsets, status, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from admin_panel.model import ministry, settings
from . import serializers
from .. import pagination


class RectorCongratulationView(viewsets.ModelViewSet):
    queryset = ministry.RectorCongratulation.objects.all()
    serializer_class = serializers.RectorCongratulationSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        instance = self.queryset.last()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)
        main = serializers.RectorCongratulationSerializer(instance).data
        return Response(main, status=status.HTTP_200_OK)


class StatisticView(viewsets.ModelViewSet):
    queryset = ministry.Statistic.objects.all()
    serializer_class = serializers.StatisticSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request):
        instance = self.queryset.last()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)

        main = serializers.StatisticSerializer(instance).data
        items = serializers.StatisticItemSerializer(ministry.StatisticItem.objects.all()[:8], many=True).data
        did_you_know = serializers.StatisticContentItemSerializer(ministry.StatisticContentItem.objects.all(),
                                                                  many=True).data
        dict = {"main": main, "items": items, "did_you_know": did_you_know}
        return Response(dict, status=status.HTTP_200_OK)


class AboutUsView(viewsets.ModelViewSet):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AboutUsSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request):
        instance = self.queryset.last()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)

        about = serializers.AboutUsSerializer(instance).data
        dict = {
            "about": about,
        }
        return Response(dict, status=status.HTTP_200_OK)


class AnnouncementView(viewsets.ModelViewSet):
    queryset = ministry.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerailizer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request):
        instance = self.queryset.last()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)
        announcement = serializers.AnnouncementSerailizer(instance).data
        return Response(announcement, status=status.HTTP_200_OK)


class GoalView(viewsets.ModelViewSet):
    queryset = ministry.Goal.objects.all()
    serializer_class = serializers.GoalSerializer
    pagination_class = None
    http_method_names = ["get"]

    def list(self, request):
        instance = self.queryset.last()
        if not instance:
            return Response({}, status=status.HTTP_200_OK)
        instance.views += 1
        instance.save()
        goal = self.serializer_class(instance).data
        dict = {
            "goal": goal,
        }
        return Response(dict, status=status.HTTP_200_OK)


class StructureView(viewsets.ModelViewSet):
    queryset = ministry.Structure.objects.all()
    serializer_class = serializers.StructureSerializer
    pagination_class = None
    http_method_names = ["get"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.serializer_class
        return Response(serializer(instance).data)


class DepartmentView(viewsets.ModelViewSet):
    queryset = ministry.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer
    pagination_class = None
    http_method_names = ["get"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.DepartmentDetailSerializer
        return serializers.DepartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer_class()
        return Response(serializer(instance).data)


class DepartmentStaffView(generics.RetrieveAPIView):
    serializer_class = serializers.DepartmentStaffSerializer
    queryset = ministry.Staff.objects.all()


class DepartmentInfoListCreateView(generics.ListCreateAPIView):
    serializer_class = serializers.DepartmentAdminInfoInlineSerializer
    pagination_class = None

    def get_queryset(self):
        return ministry.DepartmentInfo.objects.filter(department__id=self.kwargs["department_id"]).order_by("order")


class DepartmentInfoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.DepartmentAdminInfoInlineSerializer

    def get_queryset(self):
        return ministry.DepartmentInfo.objects.all()


class DepartmentMainPageView(DepartmentView):
    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(main_page=True)[:8]
        return Response(self.get_serializer(queryset, many=True).data)


class StaffView(viewsets.ModelViewSet):
    # sending only leaders in the company
    queryset = ministry.Staff.objects.all().filter(leader=True)
    # serializer_class = serializers.StaffSerializer
    pagination_class = None
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.StaffSerializer
        return serializers.StaffListSerializer


class StudyProgramView(viewsets.ModelViewSet):
    queryset = ministry.StudyProgram.objects.all().order_by("-publish_date")
    serializer_class = serializers.StudyProgramListSerializer
    pagination_class = None
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.StudyProgramDetailSerializer
        return serializers.StudyProgramListSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class TopStudyProgramView(viewsets.ReadOnlyModelViewSet):
    queryset = ministry.StudyProgram.objects.filter(main_page=True).order_by("-publish_date")
    serializer_class = serializers.StudyProgramListSerializer
    pagination_class = None
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.StudyProgramDetailSerializer
        return serializers.StudyProgramListSerializer

    def list(self, request, *args, **kwargs):
        index_serializer = serializers.TopStudyProgramListSerializer
        queryset = self.queryset[:6]
        return Response(index_serializer(queryset, many=True).data, status=200)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views = instance.views + 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class NightProgramView(viewsets.ModelViewSet):
    queryset = ministry.NightProgram.objects.all()
    serializer_class = serializers.NightProgramSerializer
    pagination_class = None
    http_method_names = ["get"]


class KafedraView(viewsets.ModelViewSet):
    queryset = ministry.Kafedra.objects.all()
    serializer_class = serializers.KafedraListSerializer
    # pagination_class = pagination.Middle
    http_method_names = ["get"]
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["faculty__slug"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.KafedraDetailSerializer
        return serializers.KafedraListSerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         kafedralar = self.get_serializer(page, many=True).data
    #     else:
    #         kafedralar = self.get_serializer(queryset, many=True).data
    #     faculty = serializers.KafedraFacultySerializer(
    #         ministry.Department.objects.filter(kafedralar__isnull=False),
    #         many=True).data
    #     payload = {
    #         'kafedra': kafedralar,
    #         'faculty': faculty
    #     }
    #
    #     return Response(payload)


class OrganizationView(viewsets.ModelViewSet):
    queryset = ministry.Organization.objects.all()
    serializer_class = serializers.OrganizationListSerializer
    # pagination_class = None
    http_method_names = ["get"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.OrganizationDetailSerializer
        return serializers.OrganizationListSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        payload = {
            "centers": serializer(self.get_queryset().filter(org_type=1), many=True).data,
            "department": serializer(self.get_queryset().filter(org_type=2), many=True).data,
            "departments": serializer(self.get_queryset().filter(org_type=3), many=True).data,
        }

        return Response(payload)


class UstavViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = ministry.Ustav.objects.all()
    serializer_class = serializers.UstavSerailizer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        try:
            ustav = ministry.UnversityFile.objects.get(slug="ustav")
        except ministry.UnversityFile.DoesNotExist:
            ustav = ministry.UnversityFile.objects.create(slug="ustav")
        payload = {"results": serializer(self.get_queryset(), many=True).data, "fayl": ustav.file_url}

        return Response(payload)


class CouncilStaffListViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = ministry.CouncilStaff.objects.all()
    serializer_class = serializers.CouncilStaffListSerializer


class CouncilListView(generics.ListAPIView):
    queryset = ministry.Council.objects.all()
    serializer_class = serializers.CouncilListSerializer
    pagination_class = LimitOffsetPagination


class CouncilDetailView(generics.RetrieveAPIView):
    queryset = ministry.Council.objects.all()
    serializer_class = serializers.CouncilListSerializer


#
# class CampListViewSet(viewsets.GenericViewSet, generics.ListAPIView):
#     queryset = ministry.Camp.objects.all()
#     serializer_class = serializers.CampSerilizer


class FamousGraduateViewSet(viewsets.ModelViewSet):
    queryset = ministry.FamousGraduate.objects.all()
    serializer_class = serializers.FamousGraduateListSerailizer
    pagination_class = pagination.Middle
    lookup_field = "slug"
    http_method_names = ["get"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.FamousGraduateDetailSerailizer
        return serializers.FamousGraduateListSerailizer


class FamousGraduateGalleryViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = ministry.FamousGraduateGallery.objects.all()
    serializer_class = serializers.FamousGraduateGallerySerailizer
    http_method_names = ["get"]
    pagination_class = pagination.ExtraMiddle

    def get_queryset(self):
        queryset = ministry.FamousGraduateGallery.objects.filter(
            famousgraduate__slug=self.kwargs.get("famousgraduate_slug", None)
        )
        return queryset


class FamousGraduateMainViewSet(FamousGraduateViewSet):
    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.FamousGraduateDetailSerailizer
        return serializers.FamousGraduateMainSerailizer


class UnversityCatalogSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = ministry.AboutMinistry.objects.all()
    serializer_class = serializers.AboutUsSerializer

    def list(self, request, *args, **kwargs):
        if ministry.AboutMinistry.objects.last():
            file = ministry.AboutMinistry.objects.last()
        else:
            file = ministry.AboutMinistry.objects.create()
        payload = {"file_url": file.file.url}

        return Response(payload)


# FAQQuestionSerializer

class FAQQuestionListView(generics.ListAPIView):
    queryset = settings.FAQQuestion.objects.all()
    serializer_class = serializers.FAQQuestionSerializer
