from django_filters.rest_framework import FilterSet, filters

from syllabus.models import CourseLesson


class CourseLessonFilterSet(FilterSet):
    syllabus = filters.NumberFilter(field_name="course_syllabus__id")

    class Meta:
        model = CourseLesson
        fields = {
            "title": ["exact", "icontains"],
        }
