from rest_framework import generics

from admin_panel.model.static import History
from api.history.serializers import HistorySerializer


class HistoryListAPIView(generics.ListAPIView):
    queryset = History.objects.order_by("order")
    serializer_class = HistorySerializer


__all__ = ["HistoryListAPIView"]
