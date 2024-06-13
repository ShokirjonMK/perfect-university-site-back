from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from admin_panel.model import docs
from api import pagination
from . import serializers
from rest_framework.decorators import api_view


class DocsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = docs.Docs.objects.all()
    serializer_class = serializers.DocsSerializer
    pagination_class = pagination.Middle

    # filter_backends = [DjangoFilterBackend, SearchFilter]


class ReportListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = docs.Report.objects.all()
    serializer_class = serializers.ReportSerializer
    pagination_class = pagination.ExtraShort


class LawyerPageView(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = docs.LawyerPage.objects.all()
    serializer_class = serializers.LawyerPageSerializer
    pagination_class = pagination.Middle


@api_view(["GET"])
def counter(request, pk):
    page = docs.LawyerPage.objects.get(pk=pk)
    if page:
        page.views = page.views + 1
        page.save()
        return Response(data={"id": page.id, "views": page.views}, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
