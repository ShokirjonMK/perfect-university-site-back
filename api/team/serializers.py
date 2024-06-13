from rest_framework import serializers
from admin_panel.model import ministry


class TeamMemberGallery(serializers.ModelSerializer):
    class Meta:
        model = ministry.StaffGallery
        fields = ("image",)


class TeamListSerializer(serializers.ModelSerializer):
    gallery = TeamMemberGallery(many=True)

    class Meta:
        model = ministry.Staff
        fields = (
            "id",
            "name",
            "title",
            "position",
            "rector",
            "image",
            "leader",
            "phone_number",
            "email",
            "reception_days",
            "bio",
            "task",
            "gallery",
        )
        read_only_fields = ("id",) # "name"
