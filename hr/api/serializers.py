from rest_framework import serializers
from hr import models


class IdTitleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()


class FieldSerializer(serializers.ModelSerializer):
    options = IdTitleSerializer(many=True, default=None)

    class Meta:
        fields = ["id", "title", "field_type", "placeholder", "required", "toggle", "options"]
        model = models.VacancyField


class FormFieldSerializer(serializers.ModelSerializer):
    step_2 = FieldSerializer(many=True)
    step_3 = FieldSerializer(many=True)
    step_4 = FieldSerializer(many=True)
    step_5 = FieldSerializer(many=True)
    nationalities_list = IdTitleSerializer(many=True)
    positions_list = IdTitleSerializer(many=True)

    class Meta:
        model = models.Form
        fields = ["id", "step_2", "step_3", "step_4", "step_5", "nationalities_list", "positions_list"]


class OptionsSerializer(serializers.Serializer):
    option = serializers.PrimaryKeyRelatedField(
        queryset=models.ChoiceFieldOptions.objects.all(), allow_null=True, default=None
    )
    text = serializers.CharField(allow_null=True, default=None)
    file = serializers.PrimaryKeyRelatedField(
        queryset=models.VacantFileField.objects.all(), allow_null=True, default=None
    )


class ExperienceDataSerializer(serializers.Serializer):
    date_from = serializers.DateField(allow_null=True, default=None)
    date_to = serializers.DateField(allow_null=True, default=None)
    position = serializers.CharField(allow_null=True, default=None)
    name = serializers.CharField(allow_null=True, default=None)


class FieldCreateSerializer(serializers.Serializer):
    field = serializers.PrimaryKeyRelatedField(queryset=models.VacancyField.objects.all())
    text = serializers.CharField(allow_null=True, default=None)
    date = serializers.DateField(allow_null=True, default=None)
    file = serializers.PrimaryKeyRelatedField(
        queryset=models.VacantFileField.objects.all(), allow_null=True, default=None
    )
    option = serializers.PrimaryKeyRelatedField(
        queryset=models.ChoiceFieldOptions.objects.all(), allow_null=True, default=None
    )
    checkbox_options = serializers.PrimaryKeyRelatedField(
        queryset=models.ChoiceFieldOptions.objects.all(), allow_null=True, default=None, many=True, allow_empty=True
    )
    options = OptionsSerializer(many=True, allow_empty=True, allow_null=True, default=[])
    experience_data = ExperienceDataSerializer(many=True, allow_empty=True, allow_null=True, default=[])

    # options = serializers.PrimaryKeyRelatedField(queryset=models.ChoiceFieldOptions.objects.all(),
    # allow_null=True,many=True, allow_empty=True)

    def validate(self, data):
        if data.get("field").required and not any(
            [
                data.get("text"),
                data.get("date"),
                data.get("option"),
                data.get("file"),
                data.get("options"),
                data.get("checkbox_options"),
            ]
        ):
            raise serializers.ValidationError({"message": "one of (text,date,option,file) fields is mandatory"})
        return data


class VacantCreateSerializer(serializers.ModelSerializer):
    fields = FieldCreateSerializer(many=True)
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = models.Vacant
        fields = [
            "id",
            "form",
            "first_name",
            "last_name",
            "middle_name",
            "date_of_birth",
            "gender",
            "nationality",
            "phone_number",
            "email",
            "address",
            "photo",
            "position",
            "vacancy",
            "fields",
        ]


class VacantFileFieldSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        fields = ["id", "file"]
        model = models.VacantFileField
        extra_kwargs = {
            "file": {"write_only": True},
        }


class NewVacantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.NewVacant
        fields = [
            "id",
            "phone_number",
            "vacancy",
            "resume_file",
        ]
