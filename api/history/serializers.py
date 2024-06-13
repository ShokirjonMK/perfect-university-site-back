from admin_panel.model.static import HistoryImage, History, HistoryYear, HistoryItem
from rest_framework import serializers


class HistoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryItem
        fields = ('id', 'content')


class HistoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryImage
        fields = ('id', 'image')


class HistoryYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryYear
        fields = ('id', 'title', 'description', 'year')


class HistorySerializer(serializers.ModelSerializer):
    history_image = HistoryImageSerializer(many=True, read_only=True)
    history_year = HistoryYearSerializer(many=True, read_only=True)
    history_item = HistoryItemSerializer(many=True, read_only=True)

    class Meta:
        model = History
        fields = ('id', 'title', 'description', 'history_image', 'history_year', 'history_item', 'order')
