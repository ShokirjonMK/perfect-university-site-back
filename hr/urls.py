from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "vacancy"


urlpatterns = [
    path("", login_required(views.JobsList.as_view()), name="jobs-list"),
    path("create/", login_required(views.JobsCreate.as_view()), name="jobs-create"),
    path("update/<int:pk>/", login_required(views.JobsUpdate.as_view()), name="jobs-update"),
    path("delete/<int:pk>/", login_required(views.JobsDelete.as_view()), name="jobs-delete"),
    path("forms/", login_required(views.VacancyFormList.as_view()), name="form-list"),
    path("forms/create/", login_required(views.VacancyFormCreate.as_view()), name="form-create"),
    path("forms/update/<int:pk>/", login_required(views.VacancyFormUpdate.as_view()), name="form-update"),
    path("forms/delete/<int:pk>/", login_required(views.VacancyFormDelete.as_view()), name="form-delete"),
    path("positions/", login_required(views.PositionList.as_view()), name="position-list"),
    path("positions/create/", login_required(views.PositionCreate.as_view()), name="position-create"),
    path("positions/update/<int:pk>/", login_required(views.PositionUpdate.as_view()), name="position-update"),
    path("positions/delete/<int:pk>/", login_required(views.PositionDelete.as_view()), name="position-delete"),
    path("vacants/", login_required(views.VacantList.as_view()), name="vacant-list"),
    path("vacants/<int:pk>/", login_required(views.VacantDetail.as_view()), name="vacant-detail"),
    path("vacants/update/<int:pk>/", login_required(views.VacantUpdate.as_view()), name="vacant-update"),
    path("vacants/delete/<int:pk>/", login_required(views.VacantDelete.as_view()), name="vacant-delete"),
]
