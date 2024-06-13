from django.urls import path
from . import views

urlpatterns = [
    path("fields/<int:pk>/", views.FormFieldsView.as_view(), name="vacancy-form-fields"),
    path("submit/", views.FormSubmitView.as_view(), name="vacancy-form-submit"),
    path("new-submit/", views.NewVacantView.as_view(), name="new-vacant-submit"),
    path("file-upload/", views.FileUploadView.as_view(), name="vacancy-file-upload"),
    path("file-delete/<int:pk>/", views.FileDeleteView.as_view(), name="vacancy-form-delete"),
]
