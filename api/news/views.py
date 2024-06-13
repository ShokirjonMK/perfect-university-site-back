from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from django.db.models import When, Case, IntegerField

from admin_panel.model import press_service
from api import pagination
from . import serializers


class NewsCategoryView(generics.ListAPIView):
    queryset = press_service.NewsCategory.objects.all()
    serializer_class = serializers.NewsCategorySerializer


class NewsListView(viewsets.ReadOnlyModelViewSet):
    """
    The model will be parent for the remaining secondary news class
    Its parameters will be used & inherited

    2. Include generics to use filters&search in params
    """

    queryset = press_service.News.objects.filter(is_published=True).annotate(
        main_priority=Case(
            When(main_page=True, then=1),
            default=2,
            output_field=IntegerField()
        )
    ).order_by("main_priority", "-publish_date")

    pagination_class = pagination.ExtraShort
    lookup_field = "slug"

    http_method_names = ["get"]
    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_fields = ["category__slug", "hashtag__slug", "objectives__slug"]
    search_fields = ["short_description", "title"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return serializers.NewsDetailSerializer
        return serializers.NewsListSerializer

    def retrieve(self, request, *args, **kwargs):
        # customization here
        instance = self.get_object()
        instance.views += 1
        instance.save()
        related = self.queryset.exclude(id=instance.id)[:4]
        related_serializer = serializers.NewsListSerializer

        payload = {"news": self.get_serializer(instance).data, "related": related_serializer(related, many=True).data}
        return Response(payload)


class IndexNewsListView(NewsListView):
    """
    News list for Web Index
    """

    queryset = press_service.News.objects.filter(is_published=True, main_page=True)
    pagination_class = None
    filter_backends = []
    filterset_fields = []

    def list(self, request, *args, **kwargs):
        index_serializer = serializers.TopNewsSerializer
        queryset = self.queryset[:3]
        return Response(index_serializer(queryset, many=True).data, status=200)


#   _____ _             _
#  | ____| | ___  _ __ | | __ _ _ __
#  |  _| | |/ _ \| '_ \| |/ _` | '__|
#  | |___| | (_) | | | | | (_| | |
#  |_____|_|\___/|_| |_|_|\__,_|_|

# class ElonlarListView(viewsets.ModelViewSet, generics.ListAPIView):
#     """
#     The model will be parent for the remaining secondary elonlar class
#     Its parameters will be used & inherited
#
#     2. Include generics to use filters&search in params
#     """
#     queryset = press_service.Elonlar.objects.filter(is_published=True).order_by('-publish_date')
#     pagination_class = pagination.Middle
#
#     http_method_names = ['get']
#     filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['category__slug', 'hashtag__slug']
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return serializers.ElonlarDetailSerializer
#         return serializers.ElonlarListSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         # customization here
#         instance = self.get_object()
#         instance.views += 1
#         instance.save()
#         related = self.queryset.exclude(id=instance.id)[:3]
#         related_serializer = serializers.ElonlarListSerializer
#
#         payload = {
#             'elonlar': self.get_serializer(instance).data,
#             'related': related_serializer(related, many=True).data
#         }
#         return Response(payload)


# class IndexElonlarListView(ElonlarListView):
#     """
#     Elonlar list for Web Index
#     """
#     queryset = press_service.Elonlar.objects.filter(is_published=True, main_page=True)
#     pagination_class = None
#
#     def list(self, request, *args, **kwargs):
#         serializer = serializers.ElonlarListSerializer
#         top_serializer = serializers.TopElonlarSerializer
#         instance = self.queryset[:3]
#
#
#         return Response(serializer(instance, many=True).data, status=200)


# class NewsCategoryView(viewsets.ModelViewSet):
#     queryset = press_service.NewsCategory.objects.all()
#     serializer_class = serializers.NewsCategoryserializer
#     http_method_names = ['get']
#     pagination_class = None


# class NewsHashtagView(viewsets.ModelViewSet):
#     queryset = press_service.NewsHashtag.objects.all()
#     serializer_class = serializers.NewsHashtagserializer
#     http_method_names = ['get']
#     pagination_class = None


# FAQ type
# TYPES = (
#     (1, _('Huquqiy')),
#     (2, _('Psixologik')),
#     (3, _("O'smirlar")),
#     (4, _('Ayollar')),
# )


class FAQListView(viewsets.ModelViewSet):
    queryset = press_service.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
    pagination_class = None
    http_method_names = ["get"]
    filter_backends = [SearchFilter]
    search_fields = ["title"]
    #
    # def list(self, request):
    #     instance = self.get_queryset().order_by("?").first()
    #     return Response(self.serializer_class(instance).data)


class ObjectiveListView(generics.ListAPIView):
    serializer_class = serializers.ObjectiveSerializer
    queryset = press_service.Objective.objects.all().order_by("number")


class ObjectiveDetailView(generics.RetrieveAPIView):
    serializer_class = serializers.ObjectiveSerializer
    queryset = press_service.Objective.objects.all()
    lookup_field = "slug"
