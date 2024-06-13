from rest_framework import serializers
from hr import models


class PositionTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = "__all__"
        model = models.Position


class NationalityTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = "__all__"
        model = models.Nationality


class JobTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        fields = "__all__"
        model = models.Job


class VacantStatusTransferSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ["status"]
        model = models.NewVacant


class CreateFormOptionTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ChoiceFieldOptions
        fields = ["title_uz", "title_ru", "title_en"]


class CreateFormFieldTransferSerializer(serializers.ModelSerializer):
    options = CreateFormOptionTransferSerializer(many=True, allow_null=True, default=[])

    class Meta:
        model = models.VacancyField
        fields = [
            "title_uz",
            "title_ru",
            "title_en",
            "placeholder_uz",
            "placeholder_ru",
            "placeholder_en",
            "field_type",
            "required",
            "toggle",
            "step",
            "options",
        ]

        extra_kwargs = {
            "title_uz": {"required": True},
            "required": {"required": True},
            "toggle": {"required": True},
        }


class CreateFormTransferSerializer(serializers.ModelSerializer):
    fields = CreateFormFieldTransferSerializer(many=True)

    class Meta:
        model = models.Form
        fields = ["id", "title", "positions", "fields"]

    def create(self, validated_data):
        fields = validated_data.pop("fields")
        positions = validated_data.pop("positions")
        instance = self.Meta.model.objects.create(**validated_data)
        instance.positions.set(positions)
        for field in fields:
            options = field.pop("options")
            field_instance = models.VacancyField.objects.create(form_id=instance.id, **field)
            if options:
                for option in options:
                    models.ChoiceFieldOptions.objects.create(field_id=field_instance.id, **option)
        return instance

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")
        if instance.title != validated_data.get("title"):
            instance.title = validated_data.get("title")
            instance.save(update_fields=["title"])
        instance.positions.set(positions)
        fields = validated_data.pop("fields")
        instance.fields.all().delete()
        for field in fields:
            options = field.pop("options")
            field_instance = models.VacancyField.objects.create(form_id=instance.id, **field)
            if options:
                for option in options:
                    models.ChoiceFieldOptions.objects.create(field_id=field_instance.id, **option)
        return instance


class VacantFileTransferFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        fields = ["id", "file"]
        model = models.VacantFileField
        extra_kwargs = {
            "file": {"write_only": True},
        }


class CreateJobCategoryTransferSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = models.JobCategory
        fields = "__all__"


# class VacantFieldValueTransferSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#
#     class Meta:
#         model = models.VacantFieldValue
#         fields = ['id', 'parent', 'step', 'title', 'field_type', 'value']
#
#
# class VacantTransferSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField()
#     fields = VacantFieldValueTransferSerializer(many=True)
#
#     class Meta:
#         model = models.Vacant
#         fields = ['id', 'status', 'form', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'gender',
#                   'nationality', 'phone_number', 'email', 'address', 'photo_url', 'position', 'fields']
#
#     def create(self, validated_data):
#         fields = validated_data.pop('fields')
#         fields = validated_data.pop('photo_url')
#         instance = self.Meta.model.objects.create(**validated_data)
#         instance.positions.set(positions)
#         for field in fields:
#             options = field.pop('options')
#             field_instance = models.VacancyField.objects.create(form_id=instance.id, **field)
#             if options:
#                 for option in options:
#                     models.ChoiceFieldOptions.objects.create(field_id=field_instance.id, **option)
#         return instance
