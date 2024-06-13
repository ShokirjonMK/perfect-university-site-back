from rest_framework import viewsets, generics
from . import serializers
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication


class TypoView(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = serializers.TypoSerializer
    pagination_class = None
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]
    http_method_names = ["post"]
