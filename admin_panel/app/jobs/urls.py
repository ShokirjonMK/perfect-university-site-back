from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", login_required(views.JobsList.as_view()), name="jobs-list"),
    path("create/", login_required(views.JobsCreate.as_view()), name="jobs-create"),
    path("update/<int:pk>/", login_required(views.JobsUpdate.as_view()), name="jobs-update"),
    path("delete/<int:pk>/", login_required(views.JobsDelete.as_view()), name="jobs-delete"),
]
