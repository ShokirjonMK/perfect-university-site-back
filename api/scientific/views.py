from rest_framework import viewsets

from admin_panel.model.scientific import ScientificJournalDesc, ScientificJournal
from api.pagination import ExtraShort
from api.scientific import serializers


class ScientificJournalDescListApiView(viewsets.ModelViewSet):
    queryset = ScientificJournalDesc.objects.all()
    serializer_class = serializers.ScientificJournalDescSerializer
    pagination_class = ExtraShort
    http_method_names = ["get"]


class ScientificJournalListApiView(viewsets.ModelViewSet):
    queryset = ScientificJournal.objects.all()
    serializer_class = serializers.ScientificJournalSerializer
    pagination_class = ExtraShort
    http_method_names = ["get"]
