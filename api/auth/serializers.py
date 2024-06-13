from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from admin_panel.model.courses import Admission
from django.db.transaction import atomic
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
import re

from admin_panel.model.territorial import Country, Nationality
from admin_panel.model.user import CustomUser
from api.utils.cache import CacheTypes
from phonenumber_field.serializerfields import PhoneNumberField

from syllabus.api_endpoints.course_syllabus.CourseSyllabusList.serializers import CustomUserSerializer


class AdmissionDataSerializer(serializers.ModelSerializer):
    nationality = serializers.CharField(source="nationality.title")
    citizenship = serializers.CharField(source="citizenship.title")

    class Meta:
        model = Admission
        fields = (
            "first_name", "last_name", "gender",
            "date_of_birth", "nationality",
            "citizenship", "phone_number",
            "education_name", "certificate",
            "graduation_year", "document_series_number",
            "diploma", "language_qualifications", "have_higher_education",
            "higher_education_name", "national_olympiads",
            "disability", "need_dormitory", "region", "start_date", "end_date"
        )


class ProfileSerializer(serializers.ModelSerializer):
    admission_fields = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "admission_fields", "email", "image")

    def get_admission_fields(self, obj):
        try:
            return AdmissionDataSerializer(obj.custom_user.admission_user,
                                   context={"request": self.context.get("request")}).data
        except Admission.DoesNotExist:
            return None

    def get_image(self, obj):
        request = self.context.get('request')
        if request and obj.custom_user.image:
            absolute_uri = request.build_absolute_uri(obj.custom_user.image.url)
            return absolute_uri
        return None


class UpdateAdmissionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admission
        fields = (
            "first_name", "last_name", "gender",
            "date_of_birth", "nationality",
            "citizenship", "phone_number",
        )
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
            "gender": {"required": False},
            "date_of_birth": {"required": False},
            "nationality": {"required": False},
            "citizenship": {"required": False},
            "phone_number": {"required": False},
        }


class ProfileUpdateSerializer(serializers.ModelSerializer):
    image = serializers.FileField(required=False)
    admission_fields__first_name = serializers.CharField(required=False)
    admission_fields__last_name = serializers.CharField(required=False)
    admission_fields__gender = serializers.IntegerField(required=False)
    admission_fields__date_of_birth = serializers.DateField(required=False)
    admission_fields__citizenship = serializers.IntegerField(required=False)
    admission_fields__phone_number = serializers.CharField(required=False)
    admission_fields__nationality = serializers.IntegerField(required=False)
    admission_fields__start_date = serializers.DateField(required=False)
    admission_fields__end_date = serializers.DateField(required=False)

    class Meta:
        model = User
        fields = ("id",
                  "admission_fields__first_name",
                  "admission_fields__last_name",
                  "admission_fields__gender",
                  "admission_fields__date_of_birth",
                  "admission_fields__citizenship",
                  "admission_fields__phone_number",
                  "admission_fields__nationality",
                  "admission_fields__start_date",
                  "admission_fields__end_date",
                  "email",
                  "image",
                  )

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        admission_info = {}
        admission_fields = [
            "admission_fields__first_name", "admission_fields__last_name",
            "admission_fields__gender", "admission_fields__date_of_birth",
            "admission_fields__citizenship", "admission_fields__phone_number",
            "admission_fields__nationality", "admission_fields__start_date",
            "admission_fields__end_date"
        ]

        for admission_field in admission_fields:
            if admission_field in validated_data:
                admission_info[admission_field.split('__', 1)[1]] = validated_data.get(admission_field)

        admission_serializer = UpdateAdmissionDataSerializer(data=admission_info)
        if admission_serializer.is_valid():
            admission_instance = instance.custom_user.admission_user
            for key, value in admission_info.items():
                if key == "citizenship":
                    value = Country.objects.get(id=value)
                if key == "nationality":
                    value = Nationality.objects.get(id=value)
                setattr(admission_instance, key, value)
            admission_instance.save()
        else:
            raise serializers.ValidationError(admission_serializer.errors, code="invalid_admission_data")

        image = validated_data.get("image")
        if image:
            instance.custom_user.image = image
            instance.custom_user.save()

        return instance

    def to_representation(self, instance):
        instance.image = instance.custom_user.image
        return super().to_representation(instance)


class RegisterSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get("email")
        if email and (User.objects.filter(email=email).exists() or User.objects.filter(username=email).exists()):
            raise serializers.ValidationError({"email": "Email already exists"}, code="email_exists")
        return data

    @atomic
    def create(self, validated_data):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(email=email, username=email)
        user.set_password(password)
        user.save()
        CustomUser.objects.create(user=user)
        return user

    def get_id(self, obj):
        return obj.custom_user.id


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                data["user"] = user
            else:
                raise serializers.ValidationError({"email": "Invalid email or password"}, code="invalid_credentials")
        else:
            raise serializers.ValidationError({"email": "This field is required"}, code="required")
        return data

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    type = serializers.CharField(required=True)

    def validate_type(self, value):
        if value not in CacheTypes.get_verification_types():
            raise serializers.ValidationError({"type": "Invalid type"}, code="invalid_type")
        return value

    def validate(self, data):
        email = data.get("email")

        verification_type = data.get("type")

        if verification_type == CacheTypes.reset_password_verification:
            query_lookup = Q(email=email)
            if not User.objects.filter(query_lookup).exists():
                raise serializers.ValidationError({"email": "Invalid email"}, code="invalid_email")

        return data


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    session = serializers.CharField(required=False)
    code = serializers.CharField(required=True, max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255, required=True)
    session = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8, max_length=32)

    def validate_password(self, new_password):
        if not re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,32}$", new_password):
            raise serializers.ValidationError(
                detail={
                    "password": _(
                        "Password must be at least 10 characters long and "
                        "contain at least one uppercase letter, one lowercase letter and one number!"
                    )
                },
                code="invalid",
            )

        return new_password
