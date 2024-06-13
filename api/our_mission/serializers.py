from rest_framework import serializers

from admin_panel.model.static import OurMission, OurMissionItem


class OurMissionItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = OurMissionItem
        fields = ("id", "title")


class OurMissionModelSerializer(serializers.ModelSerializer):
    mission_item = OurMissionItemModelSerializer(many=True, read_only=True)

    class Meta:
        model = OurMission
        fields = ("id", "title", "description", "is_main", "mission_item", "image")
