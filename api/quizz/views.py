from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api import pagination
from . import serializers
from admin_panel.model import question


class QuizzListView(viewsets.ModelViewSet):
    queryset = question.Quizz.objects.filter(is_published=True)
    serializer_class = serializers.QuizzSerializer
    pagination_class = pagination.ExtraShort
    http_method_names = ["get", "post"]

    def retrieve(self, request, *args, **kwargs):
        serializer = serializers.QuizzDetailSerializer
        # check if user already exists in question result model
        instance = self.get_object()
        payload = {
            "quizz": serializer(instance).data,
        }
        return Response(payload)

    @action(detail=True, methods=["post"])
    def answer(self, request, *args, **kwargs):
        data = self.request.data
        instance = self.get_object()
        question.QuestionResult.objects.create(question_id=data["question"], quizz=instance)
        question_instance = question.Question.objects.get(id=int(data["question"]))
        question_instance.count += 1
        question_instance.save()
        payload = {
            "quizz": serializers.QuizzDetailSerializer(instance).data,
        }
        return Response(payload, status=status.HTTP_201_CREATED)


class QuizzView(QuizzListView):
    queryset = question.Quizz.objects.filter(main_page=True, is_published=True)
    pagination_class = None
    serializer_class = serializers.QuizzDetailSerializer

    def list(self, request, *args, **kwargs):
        instance = self.queryset.order_by("?").last()
        serializer = self.get_serializer_class()
        if not instance:
            instance = {}
        else:
            instance = serializer(instance).data
        payload = {
            "quizz": instance,
        }
        return Response(payload)


class ApplicationView(generics.CreateAPIView):
    queryset = question.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer
