from django_filters.rest_framework import FilterSet, filters

from syllabus.models import CourseLessonResource


class CourseLessonResourceFilterSet(FilterSet):
    syllabus = filters.NumberFilter(field_name="course_syllabus__id")

    class Meta:
        model = CourseLessonResource
        fields = {}
