import django_filters
from admin_panel.model import science


class FilterByyear(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="start_date", lookup_expr="year")

    class Meta:
        model = science.ConferenceSubject
        fields = ["year"]
