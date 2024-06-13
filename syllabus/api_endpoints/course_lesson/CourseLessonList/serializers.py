from rest_framework import serializers

from syllabus.models import CourseLesson, CourseLessonHour


class CourseLessonHourSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseLessonHour
        fields = ["id", "type", "hour"]


class CourseLessonSerializer(serializers.ModelSerializer):
    course_lesson_hours = CourseLessonHourSerializer(many=True)

    class Meta:
        model = CourseLesson
        fields = ["id", "title", "lesson_goals", "course_syllabus", "order", "course_lesson_hours"]

