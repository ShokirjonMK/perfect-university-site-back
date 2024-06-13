from rest_framework import serializers

from admin_panel.model.scientific import ScientificJournal, ScientificJournalDesc
from api.serializers import ThumbnailImageSerializer


class ScientificJournalSerializer(serializers.ModelSerializer):
    image_url = ThumbnailImageSerializer(source="image", read_only=True)

    class Meta:
        model = ScientificJournal
        fields = ("id", "title", "description", "file", "image_url", "date")


class ScientificJournalDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScientificJournalDesc
        fields = ("id", "title", "description")
