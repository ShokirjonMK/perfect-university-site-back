from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

from hr import models
from . import serializers


class CreateView(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(id=request.data.get("id"))
        except:
            instance = None
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class PositionCreateView(CreateView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionTransferSerializer


class PositionUpdateView(generics.UpdateAPIView):
    queryset = models.Position.objects.all()
    serializer_class = serializers.PositionTransferSerializer


class PositionDeleteView(generics.DestroyAPIView):
    queryset = models.Position.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class NationalityCreateView(CreateView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalityTransferSerializer


class NationalityUpdateView(generics.UpdateAPIView):
    queryset = models.Nationality.objects.all()
    serializer_class = serializers.NationalityTransferSerializer


class NationalityDeleteView(generics.DestroyAPIView):
    queryset = models.Nationality.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class JobCreateView(CreateView):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobTransferSerializer


class JobUpdateView(generics.UpdateAPIView):
    queryset = models.Job.objects.all()
    serializer_class = serializers.JobTransferSerializer


class JobDeleteView(generics.DestroyAPIView):
    queryset = models.Job.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class FormCreateView(CreateView):
    queryset = models.Form.objects.all()
    serializer_class = serializers.CreateFormTransferSerializer

    def post(self, request):
        print(request.data)
        return super().post(request)


class FormUpdateView(generics.UpdateAPIView):
    queryset = models.Form.objects.all()
    serializer_class = serializers.CreateFormTransferSerializer

    def put(self, request, *args, **kwargs):
        print(request.data)
        return super().put(request, *args, **kwargs)


class JobCategoryCreateView(CreateView):
    queryset = models.JobCategory.objects.all()
    serializer_class = serializers.CreateJobCategoryTransferSerializer


class JobCategoryUpdateView(generics.UpdateAPIView):
    queryset = models.JobCategory.objects.all()
    serializer_class = serializers.CreateJobCategoryTransferSerializer


class JobCategoryDeleteView(generics.DestroyAPIView):
    queryset = models.JobCategory.objects.all()
    lookup_field = "pk"


class VacantUpdateView(generics.UpdateAPIView):
    queryset = models.NewVacant.objects.all()
    serializer_class = serializers.VacantStatusTransferSerializer


class VacantDeleteView(generics.DestroyAPIView):
    queryset = models.NewVacant.objects.all()


class FileUploadView(CreateView):
    serializer_class = serializers.VacantFileTransferFieldSerializer
    queryset = models.VacantFileField.objects.all()


class FileDeleteView(generics.DestroyAPIView):
    queryset = models.VacantFileField.objects.all()

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
