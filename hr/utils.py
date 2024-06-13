import json

from django.utils.text import slugify

# GENERATE UNIQUE SLUG
from . import translate


# Auto generate model
def generate_field(field):
    try:
        result = translate.translate_to_latin(field)
        return result
    except Exception:
        pass


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    if not origin_slug:
        origin_slug = slugify(generate_field(field))
    unique_slug = origin_slug
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug


# Simple boolean checke for HTML checker
def boolen_checker(value):
    if value == "on":
        return True
    return False


def cool_print(json_data):
    print(json.dumps(json_data, indent=4, ensure_ascii=False))
