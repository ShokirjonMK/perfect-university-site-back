from rest_framework import serializers

from syllabus.models import StudentAssessment


class StudentAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAssessment
        fields = ("rating_assessment", "max_ball", "task_to_be_completed", "task_completion_time")
