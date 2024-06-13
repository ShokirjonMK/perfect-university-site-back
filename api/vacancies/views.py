from rest_framework import generics
from . import serializers
from admin_panel.model import vacancies as models
from rest_framework.response import Response
from admin_panel.model import territorial
from rest_framework import status
from django.db import transaction
from rest_framework.parsers import MultiPartParser, FormParser


class FormFieldsView(generics.RetrieveAPIView):
    serializer_class = serializers.FormFieldSerializer
    queryset = models.Form.objects.all()

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        payload = {
            "id": instance.pk,
            "step_2": instance.fields.filter(step=2),
            "step_3": instance.fields.filter(step=3),
            "step_4": instance.fields.filter(step=4),
            "nationalities_list": territorial.Nationality.objects.values("id", "title"),
            "positions_list": instance.positions.values("id", "title"),
        }
        serializer = self.get_serializer(payload)
        return Response(serializer.data)


class FormSubmitView(generics.CreateAPIView):
    """one of (text,date,option,options,file) fields is mandatory in fields array"""

    serializer_class = serializers.VacantCreateSerializer
    queryset = models.Vacant.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        fields = validated_data.pop("fields")
        form = validated_data.get("form")
        form_fields = form.fields.values_list("id", flat=True)
        message = "Simple"
        if len(form_fields) != len(fields):
            return Response({"message": "fields not complete"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                instance = self.queryset.model.objects.create(**validated_data)
                for field_object in fields:
                    field = field_object.get("field")
                    if field.id not in form_fields:
                        message = f" field({field.id}) is not in the form fields"
                        raise ValueError
                    value = None
                    if field.field_type < 4:
                        value = field_object.get("text")
                    if field.field_type == 4:
                        value = field_object.get("date").strftime("%Y-%m-%d")
                    elif field.field_type == 5 or field.field_type == 7:
                        value = field_object.get("option").title
                    elif field.field_type == 6:
                        file = getattr(field_object.get("file"), "file", None)
                        if file:
                            value = f'<a href="{file.url}">{file.name}</a>'
                    elif field.field_type == 8:
                        options = field_object.get("checkbox_options")
                        value = ""
                        for option in options:
                            value = f"{value}{option.title_uz}, "
                        value = value[:-2]
                    if value:
                        models.VacantFieldValue.objects.create(
                            vacant=instance,
                            step=field.step,
                            title=field.title_uz,
                            field_type=field.field_type,
                            value=value,
                        )
                    elif field.field_type == 9:
                        parent = models.VacantFieldValue.objects.create(
                            vacant=instance,
                            step=field.step,
                            title=field.title_uz,
                            field_type=field.field_type,
                            value="",
                        )
                        options = field_object.get("options")
                        for option in options:
                            models.VacantFieldValue.objects.create(
                                parent=parent,
                                vacant=instance,
                                step=field.step,
                                title=option.get("option").title_uz,
                                field_type=3,
                                value=option.get("text"),
                            )
                    elif field.field_type == 10:
                        parent = models.VacantFieldValue.objects.create(
                            vacant=instance,
                            step=field.step,
                            title=field.title_uz,
                            field_type=field.field_type,
                            value="",
                        )
                        options = field_object.get("options")
                        for option in options:
                            file = option.get("file").file
                            value = f'<a href="{file.url}">{file.url}</a>'
                            models.VacantFieldValue.objects.create(
                                parent=parent,
                                vacant=instance,
                                step=field.step,
                                title=option.get("option").title_uz,
                                field_type=6,
                                value=value,
                            )
        except ValueError:
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(message, status=status.HTTP_201_CREATED)


class FileUploadView(generics.CreateAPIView):
    serializer_class = serializers.VacantFileFieldSerializer
    queryset = models.VacantFileField.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class FileDeleteView(generics.DestroyAPIView):
    queryset = models.VacantFileField.objects.all()
