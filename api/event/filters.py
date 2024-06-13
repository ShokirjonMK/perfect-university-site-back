import django_filters
from admin_panel.model.event import Event


class EventFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="start_time__date", lookup_expr="exact", label="date")
    hashtag_slug = django_filters.CharFilter(field_name="hashtag__slug", label="hashtag_slug")

    class Meta:
        model = Event
        fields = ["date", "hashtag_slug"]
