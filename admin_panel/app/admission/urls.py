from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "admission"

urlpatterns = [
    path("", login_required(views.AdmissionList.as_view()), name="admission-list"),
    path("create/", login_required(views.AdmissionCreate.as_view()), name="admission-create"),
    # path('page/', login_required(views.AdmissionPageUpdate.as_view()), name='admission-page-update'),
    path("update/<int:pk>/", login_required(views.AdmissionUpdate.as_view()), name="admission-update"),
    path("delete/<int:pk>/", login_required(views.AdmissionDelete.as_view()), name="admission-delete"),
]
