from rest_framework import serializers

from admin_panel.model import question


class QuestionSerializer(serializers.RelatedField):
    def to_representation(self, obj):

        data = {
            "id": obj.id,
            "title": obj.title,
            "percentage": obj.percentage,
            # 'count': obj.count,
        }
        return data

    # def to_internal_value(self, id):
    #     return question.Quizz.objects.get(id=id)


class QuizzSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = question.Quizz
        fields = [
            "id",
            "title",
            "result_count",
            "created_at",
        ]


class QuizzDetailSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = question.Quizz
        fields = ["id", "title", "result_count", "question", "created_at"]


class QuestionResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.QuestionResult
        fields = ["question", "quizz"]


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = question.Application
        fields = ("id", "name", "surname", "email", "file", "phone_number", "application_text")
