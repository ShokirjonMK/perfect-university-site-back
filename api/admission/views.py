from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from admin_panel.model.courses import CourseCatalog
from admin_panel.model import territorial
from . import serializers
from rest_framework.decorators import api_view


class AdmissionCreate(viewsets.ViewSet, generics.CreateAPIView):
    serializer_class = serializers.AdmissionSerializer
    pagination_class = None
    parser_classes = (MultiPartParser, FormParser)
    http_method_names = ["post"]


@api_view(["GET"])
def admission_objects(request):
    helper_list = []
    for degree in CourseCatalog.objects.all():
        helper_list.append(
            {
                "id": degree.id,
                "title": degree.title,
                "applications": degree.directions.filter(is_admission=True).values("id", "title"),
            }
        )

    context = {
        "degrees": helper_list,
        "countries": territorial.Country.objects.values("id", "title"),
        "nationalities": territorial.Nationality.objects.values("id", "title"),
    }
    return Response(context)
