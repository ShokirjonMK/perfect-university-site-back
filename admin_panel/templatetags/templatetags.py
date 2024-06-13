from django import template
from django.core.serializers import serialize
from modeltranslation.utils import get_language

from admin_panel.model.territorial import Region

register = template.Library()


@register.simple_tag(name="get_language_url")
def get_language_url(request, lang):
    active_language = get_language()
    return request.get_full_path().replace(active_language, lang, 1)


@register.simple_tag(name="get_regions")
def get_regions():
    return Region.objects.all()


@register.filter
def json(queryset):
    return serialize("json", queryset)


# @register.filter
# def json(queryset):
#     structure = json.dumps(queryset)
#     return structure
