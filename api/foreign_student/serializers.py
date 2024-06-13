from rest_framework import serializers

from admin_panel.model.ministry import ForeignStudent


class ForeignStudentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForeignStudent
        fields = ("id", "background_image", "youtube_link")
