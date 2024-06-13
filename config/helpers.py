from django.utils.text import slugify
from django.db import models
from config import translate


def generate_unique_slug(klass: models.Model, field: object) -> object:
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    if not origin_slug:
        origin_slug = slugify(generate_field(field))
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug


# UPDATING INSTANCE'S MODEL VALUES WITH GIVEN DICT
def update_object_values(obj, dictx):  # requires object and dictionary. Set values to the object
    image_list = ["image", "icon", "photo", "background_image"]
    for attr, value in dictx.items():

        if hasattr(obj, attr):
            if attr in image_list and attr is None:
                pass
            else:
                setattr(obj, attr, value)
    obj.save()


# GENERATING UNIQUE ID
# def unique_number_generator(klass, length, attribute='order_number'):
def unique_number_generator(klass, length, instance, type):
    last_id = klass.objects.filter(order_number__startswith=type).exclude(id=instance.id).order_by("id").last()

    if not last_id or not last_id.order_number:  # return initial number
        initial = (length - 1) * "0" + "1"
        return initial

    number = last_id.order_number
    number = number.replace(type, "")

    number = int(number) + 1
    formatted = (length - len(str(number))) * "0" + str(number)
    return str(formatted)


# Simple boolean checke for HTML checker
def boolen_checker(value):
    if value == "on":
        return True
    return False


# Auto generate model
def generate_field(field):
    try:
        result = translate.translate_to_latin(field)
        return result
    except Exception:
        pass


# Auto generate model
def generate_field_to_cr(field):
    try:
        result = translate.translate_to_cyrillic(field)
        return result
    except Exception:
        pass
