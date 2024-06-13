from rest_framework import viewsets, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from api.science import serializers
from api import pagination
from . import filters
from admin_panel.model import science
from rest_framework import status
from django.db.models import Prefetch

from ..filters import ConferenceFilter


class MonoArticleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = science.MonoArticle.objects.filter(is_published=True)
    serializer_class = serializers.MonoArticleListSerializer

    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.MonoArticleDetailSerializer
        return serializers.MonoArticleListSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     payload_data = []
    #     for num in instance.values_list('sections__section_number',flat=True).disrinct('sections__section_number'):
    #         payload_data.append(
    #             {'section':num,
    #              'data':serializers.SectionSerializer()
    #              })


class ConferenceListView(generics.ListAPIView):
    queryset = science.PendingConference.objects.all()
    serializer_class = serializers.ConferenceListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ConferenceFilter


class ConferenceDetailView(generics.RetrieveAPIView):
    queryset = science.PendingConference.objects.all()
    serializer_class = serializers.ConferenceDetailSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConferenceApplicationCreateView(generics.CreateAPIView):
    queryset = science.ConferenceApplication.objects.all()
    serializer_class = serializers.ConferenceApplicationSerializer


class ConferenceYearsView(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = science.ConferenceSubject.objects.all()
    serializer_class = serializers.ConferenceSubjectSerializer

    def list(self, request, *args, **kwargs):
        return Response(set(self.queryset.values_list("start_date__year", flat=True)))


class ConferenceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = science.ConferenceSubject.objects.all()
    serializer_class = serializers.ConferenceSubjectSerializer
    # filter_backends = [DjangoFilterBackend]
    filter_class = filters.FilterByyear

    # filterset_fields = ['start_date']

    def list(self, request, *args, **kwargs):
        year = request.GET.get("year")
        if not year:
            Response(status=status.HTTP_204_NO_CONTENT)
        # queryset = self.filter_queryset(self.get_queryset())
        conference_ids = self.get_queryset().filter(start_date__year=year).values_list("conference_id", flat=True)
        subjects = Prefetch("subjects", self.get_queryset().filter(start_date__year=year))
        queryset = science.Conference.objects.filter(id__in=conference_ids).prefetch_related(subjects)

        serializer = serializers.YearlyConferencesSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

        # conferences = queryset.order_by('conference_id').distinct(
        #     'conference_id').values_list('conference_id',
        #                                   'conference__title')
        # payload_data = []
        # for conference in conferences:
        #     payload_data.append({
        #         'title': conference[1],
        #         'subjects': serializers.ConferenceSubjectSerializer(
        #             queryset.filter(conference_id=conference[0]).order_by(
        #                 '-start_date'),
        #             many=True,context={'request':request}).data
        #     })
        # # payload = {
        # #     'conferences': payload_data,
        # #     'years':
        # #         set(self.queryset.values_list("start_date__year", flat=True))
        # # }
        # return Response(payload_data)


class ScienceFilesViewSet(viewsets.GenericViewSet, generics.ListAPIView):
    queryset = science.ScienceFiles.objects.all()
    serializer_class = serializers.ScienceFilesSerailizer


class ScienceNewsViewSet(viewsets.ModelViewSet):
    """
    The model will be parent for the remaining secondary news class
    Its parameters will be used & inherited

    2. Include generics to use filters&search in params
    """

    queryset = science.ScienceNews.objects.filter(is_published=True)
    pagination_class = pagination.Middle
    lookup_field = "slug"

    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["category__slug", "hashtag__slug"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.ScienceNewsDetailSerializer
        return serializers.ScienceNewsListSerializer

    def retrieve(self, request, *args, **kwargs):
        # customization here
        instance = self.get_object()
        instance.views += 1
        instance.save()
        related = self.queryset.exclude(id=instance.id)[:4]
        related_serializer = serializers.ScienceNewsListSerializer

        payload = {"news": self.get_serializer(instance).data, "related": related_serializer(related, many=True).data}
        return Response(payload)


class SeminarViewSet(viewsets.ModelViewSet):
    """
    The model will be parent for the remaining secondary news class
    Its parameters will be used & inherited

    2. Include generics to use filters&search in params
    """

    queryset = science.Seminar.objects.filter(is_published=True)
    pagination_class = pagination.Middle
    lookup_field = "slug"

    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["category__slug", "hashtag__slug"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.SeminarDetailSerializer
        return serializers.SeminarListSerializer

    def retrieve(self, request, *args, **kwargs):
        # customization here
        instance = self.get_object()
        instance.views += 1
        instance.save()
        related = self.queryset.exclude(id=instance.id)[:4]
        related_serializer = serializers.SeminarRelatedListSerializer

        payload = {
            "seminars": self.get_serializer(instance).data,
            "related": related_serializer(related, many=True).data,
        }
        return Response(payload)


class ScienceCenterListView(generics.ListAPIView):
    queryset = science.ScienceCenter.objects.filter(is_published=True)
    serializer_class = serializers.ScienceCenterListSerializer
    pagination_class = LimitOffsetPagination


class ScienceCenterSingleView(generics.RetrieveAPIView):
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    queryset = science.ScienceCenter.objects.all()
    serializer_class = serializers.ScienceCenterSingleSerializer
