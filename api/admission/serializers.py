from rest_framework import serializers
from admin_panel.model.courses import Admission


class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = "__all__"
        extra_kwargs = {
            "user": {"required": True},
            "degree": {"required": False},
            "application": {"required": False},
            "education_name": {"required": False},
            "certificate": {"required": False},
            "language_qualifications": {"required": False},
            "document_series_number": {"required": False},
            "nationality": {"required": True},
            "citizenship": {"required": True},

        }
