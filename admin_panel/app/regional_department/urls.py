from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "regional_department"

urlpatterns = [
    path("", login_required(views.RegionalDepartmentList.as_view()), name="regional_department-list"),
    path(
        "update/<int:pk>/", login_required(views.RegionalDepartmentUpdate.as_view()), name="regional_department-update"
    ),
    path(
        "delete/<int:pk>/", login_required(views.RegionalDepartmentDelete.as_view()), name="regional_department-delete"
    ),
]
