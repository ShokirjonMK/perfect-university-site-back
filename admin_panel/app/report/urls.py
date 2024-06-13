from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "report"

urlpatterns = [
    path("", login_required(views.ReportList.as_view()), name="report-list"),
    path("create/", login_required(views.ReportCreate.as_view()), name="report-create"),
    path("update/<int:pk>/", login_required(views.ReportUpdate.as_view()), name="report-update"),
    path("delete/<int:pk>/", login_required(views.ReportDelete.as_view()), name="report-delete"),
]
