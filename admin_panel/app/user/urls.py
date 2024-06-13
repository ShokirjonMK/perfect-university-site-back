# from django.contrib.auth.decorators import login_required
from django.urls import path
from admin_panel.decorators import only_admin as login_required
from . import views

app_name = "user"

urlpatterns = [
    path("", login_required(views.CustomUserList.as_view()), name="user-list"),
    path("create/", login_required(views.CreateCustomUserView.as_view()), name="user-create"),
    path("update/<int:pk>/", login_required(views.UpdateCustomUserView.as_view()), name="user-update"),
    path("delete/<int:pk>/", login_required(views.CustomUserDelete.as_view()), name="user-delete"),
]
