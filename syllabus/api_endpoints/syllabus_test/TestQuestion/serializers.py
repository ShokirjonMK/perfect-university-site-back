from __future__ import annotations

from rest_framework import serializers

from syllabus.models import TestQuestion, CourseSyllabusTest, TestAnswer


class TestAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestAnswer
        fields = [
            "id",
            "answer",
        ]


class CourseSyllabusTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSyllabusTest
        fields = [
            "id",
            "course_syllabus",
        ]


class TestQuestionListSerializer(serializers.ModelSerializer):
    test = CourseSyllabusTestSerializer()
    test_answers = TestAnswerSerializer(many=True)

    class Meta:
        model = TestQuestion
        fields = ["id", "test", "question", "test_answers"]
