from itertools import chain

from rest_framework.response import Response
from rest_framework.views import APIView
from admin_panel.model import event, press_service, question
from . import serializers
from rest_framework import status


class Search(APIView):
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['query']
    def get(self, request):
        # lang_code = request.LANGUAGE_CODE
        query = self.request.GET.get("query")
        if not query:
            return Response({"error": "Your `query` param is empty"}, status=status.HTTP_400_BAD_REQUEST)
        events = event.Event.objects.filter(title__icontains=query)
        quizz = question.Quizz.objects.filter(title__icontains=query)
        news = press_service.News.objects.filter(title__icontains=query)
        photogallery = press_service.PhotoGallery.objects.filter(title__icontains=query)
        videogallery = press_service.VideoGallery.objects.filter(title__icontains=query)
        vebinar = press_service.Vebinar.objects.filter(title__icontains=query)
        # static_page = static.StaticPage.objects.filter(title__icontains=query)
        chain(
            events,
            events,
            news,
            photogallery,
            videogallery,
        )

        serializer = serializers.SearchSerializer(
            {
                "events": events,
                "quizz": quizz,
                "news": news,
                "photogallery": photogallery,
                "videogallery": videogallery,
                "vebinar": vebinar,
            },
            context={"request": request},
        )
        return Response(data=serializer.data)
