from django.urls import path
from django.contrib.auth.decorators import login_required
from hr.panel_api import views

urlpatterns = [
    path("form-create/", views.FormCreateView.as_view(), name="form-create-panel-api"),
    path("form-update/<int:pk>/", views.FormUpdateView.as_view(), name="form-update-panel-api"),
    path("image-upload/", login_required(views.HrImageUploadView.as_view()), name="hr-image-upload"),
]
