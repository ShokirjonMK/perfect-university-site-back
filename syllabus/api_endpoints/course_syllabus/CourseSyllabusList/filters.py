from django_filters.rest_framework import FilterSet, filters

from syllabus.models import CourseSyllabus


class CourseSyllabusFilterSet(FilterSet):
    year = filters.NumberFilter(field_name="year__year")

    class Meta:
        model = CourseSyllabus
        fields = {
            "title": ["exact", "icontains"],
            "syllabus": ["exact"],
        }
