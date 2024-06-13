from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from admin_panel.model import contact
from . import serializers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class ContactView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = serializers.ContactSerializer
    pagination_class = None
    http_method_names = ["post"]


class Email(viewsets.ModelViewSet, generics.CreateAPIView):
    queryset = contact.UserEmail.objects.all()
    serializer_class = serializers.EmailSerializer
    pagination_class = None
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class
        serializer = serializer(data=request.data)
        if serializer.is_valid():
            obj = contact.UserEmail.objects.create(**serializer.validated_data)
            payload = {
                "message": "Successfully saved",
                "email": obj.email,
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
