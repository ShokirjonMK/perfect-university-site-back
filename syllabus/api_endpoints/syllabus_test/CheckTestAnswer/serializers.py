from rest_framework import serializers

from syllabus.models import TestAnswer


class TestAnswerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = [
            "id",
            "is_correct",
        ]
