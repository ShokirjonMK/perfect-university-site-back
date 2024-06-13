from rest_framework import serializers
from admin_panel.model import docs
from django.utils.translation import gettext


class DocsSerializer(serializers.ModelSerializer):
    law_date = serializers.SerializerMethodField()

    class Meta:
        model = docs.Docs
        fields = ("id", "law", "law_date", "title", "number", "file")

    def get_law_date(self, obj):
        # language = get_language_from_request(self.context['request'])
        return f"{obj.date.year}, {obj.date.day} {gettext(obj.date.strftime('%B'))}"


class ReportSerializer(serializers.ModelSerializer):
    quarter = serializers.CharField(source="get_quarter_display", read_only=True)

    class Meta:
        model = docs.Report
        fields = ("id", "title", "date", "quarter", "file")


class LawyerPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = docs.LawyerPage
        fields = ("id", "title", "file_url", "views", "date")
