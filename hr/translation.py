from modeltranslation.translator import TranslationOptions, register
from . import models


@register(models.Position)
class PositionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(models.VacancyField)
class VacancyFieldTranslationOptions(TranslationOptions):
    fields = ("title", "placeholder")


@register(models.ChoiceFieldOptions)
class ChoiceFieldOptionsTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(models.Job)
class JobTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "department",
        "content",
    )


@register(models.Nationality)
class NationalityTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(models.JobCategory)
class JobCategoryTranslationOptions(TranslationOptions):
    fields = ("name",)
