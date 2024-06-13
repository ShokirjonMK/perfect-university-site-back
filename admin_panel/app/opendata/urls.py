from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "opendata"

urlpatterns = [
    path("", login_required(views.OpendataList.as_view()), name="opendata-list"),
    path("create/", login_required(views.OpendataCreate.as_view()), name="opendata-create"),
    path("update/<int:pk>/", login_required(views.OpendataUpdate.as_view()), name="opendata-update"),
    path("delete/<int:pk>/", login_required(views.OpendataDelete.as_view()), name="opendata-delete"),
    path("file/<int:pk>/", login_required(views.OpendataFileDelete.as_view()), name="file-delete"),
]
