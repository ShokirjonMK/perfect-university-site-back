import requests
from rest_framework import generics, parsers
from sentry_sdk import capture_exception

from . import serializers
from hr import models
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.conf import settings

TRANSFER_HOST = getattr(settings, "TRANSFER_HOST", "example.com")


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
            "step_5": instance.fields.filter(step=5),
            "nationalities_list": models.Nationality.objects.values("id", "title"),
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
                instance, created = self.queryset.model.objects.update_or_create(
                    id=validated_data.pop("id", None), defaults=validated_data
                )
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
                        option = field_object.get("option")
                        if option:
                            value = field_object.get("option").title
                    elif field.field_type == 6:
                        file = getattr(field_object.get("file"), "file", None)
                        if file:
                            value = file.name
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
                            if option.get("text"):
                                models.VacantFieldValue.objects.create(
                                    parent=parent,
                                    vacant=instance,
                                    step=field.step,
                                    title=option.get("option").title_uz,
                                    field_type=3,
                                    value=option.get("text", " "),
                                )
                        if not models.VacantFieldValue.objects.filter(parent=parent).exists():
                            parent.delete()
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
                            if option.get("file"):
                                file = option.get("file").file
                                value = file.name
                                models.VacantFieldValue.objects.create(
                                    parent=parent,
                                    vacant=instance,
                                    step=field.step,
                                    title=option.get("option").title_uz,
                                    field_type=6,
                                    value=value,
                                )
                        if not models.VacantFieldValue.objects.filter(parent=parent).exists():
                            parent.delete()
                    elif field.field_type == 11:
                        experience_data = field_object.get("experience_data")
                        for ex_data in experience_data:
                            models.VacantFieldValue.objects.create(
                                vacant=instance,
                                step=field.step,
                                title=ex_data.get("name"),
                                field_type=field.field_type,
                                value=ex_data.get("position"),
                                from_date=ex_data.get("date_from"),
                                from_to=ex_data.get("date_to"),
                            )
        except ValueError:
            return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        data["id"] = instance.id
        response = requests.post(f"{settings.HR_HOST}/api/v1/vacancy-form/submit/", json=data)
        text = f"Xabarni muaffaqiyatliu yubordim status kodi: {response.status_code} text:{response.text}"
        try:
            requests.post(
                f"https://api.telegram.org/bot5277163960:AAFpnia22exgu2rXGmRieIPlgpsMTM3LRNM/"
                f"sendMessage?chat_id=881319779&text={text}"
            )
        except ConnectionError:
            pass
        return Response(message, status=status.HTTP_201_CREATED)


class FileUploadView(generics.CreateAPIView):
    serializer_class = serializers.VacantFileFieldSerializer
    queryset = models.VacantFileField.objects.all()

    def post(self, request, *args, **kwargs):
        try:
            file = (request.FILES["file"].name, request.FILES["file"].file.getvalue())
        except Exception as e:
            capture_exception(e)
            file = (request.FILES["file"].name, request.FILES["file"].file)
        files = {"file": file}
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        requests.post(f"{settings.HR_HOST}/api/v1/vacancy-form/file-upload/", data=serializer.data, files=files)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FileDeleteView(generics.DestroyAPIView):
    queryset = models.VacantFileField.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        requests.delete(f"{settings.HR_HOST}/api/v1/vacancy-form/file-delete/{instance.id}/")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class NewVacantView(generics.CreateAPIView):
    serializer_class = serializers.NewVacantSerializer
    parser_classes = [parsers.MultiPartParser]
