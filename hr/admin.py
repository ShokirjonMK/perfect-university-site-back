from django.contrib import admin

from . import models


class FieldInlineAdmin(admin.StackedInline):
    model = models.VacancyField
    extra = 0


@admin.register(models.Form)
class FormAdmin(admin.ModelAdmin):
    inlines = [FieldInlineAdmin]
    list_display = ["title", "id"]
    search_fields = ["title", "id"]


class OptionInlineAdmin(admin.TabularInline):
    model = models.ChoiceFieldOptions
    extra = 0


@admin.register(models.VacancyField)
class FieldAdmin(admin.ModelAdmin):
    inlines = (OptionInlineAdmin,)
    list_display = ["title", "id"]
    list_filter = ["field_type"]
    search_fields = ["form", "title", "id"]


@admin.register(models.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    search_fields = ["title", "id"]


@admin.register(models.Nationality)
class NationalityAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    search_fields = ["title", "id"]


@admin.register(models.Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ["title", "id"]
    search_fields = ["title", "id"]


# class VacantFieldValueInlineAdmin(admin.TabularInline):
#     model = models.VacantFieldValue
#     extra = 0
#
#
# @admin.register(models.Vacant)
# class VacantAdmin(admin.ModelAdmin):
#     list_display = ["id", "first_name", "created_at", "form"]
#     search_fields = ["first_name", "last_name", "middle_name"]
#     list_filter = ["form"]
#     inlines = (VacantFieldValueInlineAdmin,)


@admin.register(models.JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "id"]
    search_fields = ["name", "id"]


@admin.register(models.VacantFileField)
class VacantFileFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(models.NewVacant)
class NewVacantAdmin(admin.ModelAdmin):
    list_display = ["id", "phone_number", "status", "vacancy", "created_at", "updated_at"]
    search_fields = ["phone_number", "vacncy__title"]
