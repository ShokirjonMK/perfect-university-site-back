from django.conf import settings
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from hr import models
from . import serializers

TRANSFER_HOST = getattr(settings, "TRANSFER_HOST", "example.com")


class FormCreateView(generics.CreateAPIView):
    queryset = models.Form.objects.all()
    serializer_class = serializers.CreateFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # requests.post(f"{TRANSFER_HOST}/hr/api/v1/form-create/", json=serializer.data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FormUpdateView(generics.UpdateAPIView):
    queryset = models.Form.objects.all()
    serializer_class = serializers.CreateFormSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # requests.put(f"{TRANSFER_HOST}/hr/api/v1/form-update/{instance.id}/", json=serializer.data)
        return Response(serializer.data)


class HrImageUploadView(generics.CreateAPIView):
    queryset = models.MediaImage.objects.all()
    serializer_class = serializers.HrMediaImageSerializer
    permission_classes = [IsAuthenticated]
