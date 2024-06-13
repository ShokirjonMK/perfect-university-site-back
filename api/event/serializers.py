from rest_framework import serializers
from admin_panel.model import event


class HashTagSerializer(serializers.RelatedField):
    def to_representation(self, value):
        obj = {
            "id": value.id,
            "title": value.title,
            "slug": value.slug,
        }
        return obj


class EventSerializer(serializers.ModelSerializer):
    # event_date = serializers.DateTimeField(format='%d %B %Y', required=False, read_only=True)
    # day = serializers.SerializerMethodField()
    # month = serializers.SerializerMethodField()
    # day_name = serializers.SerializerMethodField()
    duration = serializers.CharField()
    status = serializers.CharField()
    short_description = serializers.CharField()
    hashtag = HashTagSerializer(many=True, read_only=True)

    class Meta:
        model = event.Event
        fields = (
            "id",
            "title",
            # 'day', 'month', 'day_name',
            "event_date",
            "duration",
            "status",
            "views",
            "short_description",
            "hashtag",
        )

    # def get_day(self, obj):
    #
    #     return obj.event_date.strftime("%d")
    #
    # def get_month(self, obj):
    #     language_code = get_language_from_request(self.context['request'])
    #     print(language_code)
    #     if language_code == 'uz':
    #         return generate_field_to_cr(gettext(obj.event_date.strftime("%B")))
    #     return gettext(obj.event_date.strftime("%B"))
    #
    # def get_day_name(self, obj):
    #     language_code = get_language_from_request(self.context['request'])
    #     if language_code == 'uz':
    #         return generate_field_to_cr(gettext(obj.event_date.strftime("%A")))
    #     return gettext(obj.event_date.strftime("%A"))


class EventDetailSerializer(EventSerializer):
    class Meta:
        model = event.Event
        fields = ("id", "title", "event_date", "duration", "status", "views", "description", "hashtag")
