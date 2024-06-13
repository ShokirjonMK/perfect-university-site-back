import sys

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from rest_framework import status
from api.auth.serializers import ProfileSerializer, RegisterSerializer, LoginSerializer, VerifyResetCodeSerializer, \
    SendVerificationCodeSerializer, ResetPasswordSerializer, ProfileUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.core.cache import cache
from rest_framework.serializers import ValidationError
from django.utils.translation import gettext_lazy as _

from api.utils.cache import generate_cache_key, CacheTypes
from api.utils.verification import generate_session, generate_verification_code, send_verification_code_via_email


class UserProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserUpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUpdateSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserRegisterView(generics.GenericAPIView):
    queryset = None
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        response_data = serializer.get_tokens(user)
        return Response(response_data)


class SendVerificationCodeAPIView(APIView):
    serializer_class = SendVerificationCodeSerializer

    # TODO throttle qoshish kk

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        session = generate_session()
        verification_code = generate_verification_code()
        email_timeout_key = f"{data['type']}{data['email']}*"
        if cache.keys(email_timeout_key) and "test" not in sys.argv:
            raise ValidationError(detail={"email": _("Send auth verification code timeout!")}, code="timeout")
        cache_key = generate_cache_key(data["type"], data["email"], session)
        cache.set(email_timeout_key, True, timeout=50)
        send_verification_code_via_email(data["email"], verification_code)
        cache_data = {
            "code": verification_code,
            "is_verified": False
        }
        cache.set(cache_key, cache_data, timeout=60 * 1)
        return Response({"session": session}, status=status.HTTP_200_OK)


class VerifyResetPasswordCodeAPIView(APIView):
    serializer_class = VerifyResetCodeSerializer

    @swagger_auto_schema(request_body=VerifyResetCodeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data.get("email")

        email = str(email)
        cache_key = generate_cache_key(CacheTypes.reset_password_verification, email, data["session"])
        cache_data = cache.get(cache_key)
        if not cache_data:
            return Response({"code": _("Code is expired")}, status=status.HTTP_400_BAD_REQUEST)

        verified = False
        if not verified:
            if cache_data.get("code") != data.get("code"):
                return Response({"code": _("Invalid code")}, status=status.HTTP_400_BAD_REQUEST)
        cache_data["is_verified"] = True
        cache.set(cache_key, cache_data, timeout=60 * 30)

        return Response({"message": _("Code verified successfully")}, status=status.HTTP_200_OK)


class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(request_body=serializer_class)
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        email = data.get("email")
        session = data.get("session")
        new_password = data.get("new_password")

        cache_key = generate_cache_key(CacheTypes.reset_password_verification, email, session)
        cache_data = cache.get(cache_key)
        if not cache_data:
            raise ValidationError(detail={"session": _("Invalid session!")}, code="invalid")

        if not cache_data.get("is_verified"):
            raise ValidationError(detail={"session": _("Reset password is not verified!")}, code="not_verified")

        query_lookup = Q(email=email)
        user = get_object_or_404(User.objects.all(), query_lookup)
        user.set_password(new_password)
        user.save()

        cache.delete(cache_key)
        return Response({"message": _("Password reset successfully")}, status=status.HTTP_200_OK)
