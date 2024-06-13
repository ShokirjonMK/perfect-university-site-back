from rest_framework import serializers
from hr import models


class CreateFormOptionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = models.ChoiceFieldOptions
        fields = ["id", "title_uz", "title_ru", "title_en"]


class CreateFormFieldSerializer(serializers.ModelSerializer):
    options = CreateFormOptionSerializer(many=True, allow_null=True, default=[])
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = models.VacancyField
        fields = [
            "id",
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


class CreateFormSerializer(serializers.ModelSerializer):
    fields = CreateFormFieldSerializer(many=True)
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = models.Form
        fields = ["id", "title", "positions", "fields"]

    def create(self, validated_data):
        fields = validated_data.pop("fields")
        positions = validated_data.pop("positions")
        instance, created = self.Meta.model.objects.update_or_create(
            id=validated_data.pop("id", None), defaults=validated_data
        )
        instance.positions.set(positions)
        for field in fields:
            options = field.pop("options")
            field["form_id"] = instance.id
            field_instance, created = models.VacancyField.objects.update_or_create(
                id=field.pop("id", None), defaults=field
            )
            if options:
                for option in options:
                    option["field_id"] = field_instance.id
                    models.ChoiceFieldOptions.objects.update_or_create(id=option.pop("id", None), defaults=option)
        return instance

    def update(self, instance, validated_data):
        positions = validated_data.pop("positions")
        if instance.title != validated_data.get("title"):
            instance.title = validated_data.get("title")
            instance.save(update_fields=["title"])
        instance.positions.set(positions)
        fields = validated_data.pop("fields")
        instance.fields.all().delete()
        instance.positions.set(positions)
        for field in fields:
            options = field.pop("options")
            field["form_id"] = instance.id
            field_instance, created = models.VacancyField.objects.update_or_create(
                id=field.pop("id", None), defaults=field
            )

            if options:
                for option in options:
                    option["field_id"] = field_instance.id
                    models.ChoiceFieldOptions.objects.update_or_create(id=option.pop("id", None), defaults=option)
        return instance


class HrMediaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MediaImage
        fields = ["image"]
