# from rest_framework.filters import BaseFilterBackend
#
#
# class CategoryFilter(BaseFilterBackend):
#     """
#     Filter that only allows users to see their own objects.
#     """
#     def filter_queryset(self, request, queryset, view):
#         param = request.QUERY_PARAMS.get('category', None)
#         if param is not None:
#             return queryset.filter(category=param)
#         return queryset
import django_filters
from django_filters import filters, rest_framework
from admin_panel.model.science import PendingConference


class CustomDateFilter(filters.Filter):
    date_time = django_filters.DateTimeFilter(name="date_time", lookup_expr="gte")


class YearFilter(django_filters.NumberFilter):
    def filter(self, qs, value):
        if value:
            year_start = f"{value}-01-01"
            year_end = f"{value}-12-31"
            qs = qs.filter(date__range=[year_start, year_end])
        return qs


class ConferenceFilter(rest_framework.FilterSet):
    year = YearFilter(field_name="date")

    class Meta:
        model = PendingConference
        fields = ("year", "status")
