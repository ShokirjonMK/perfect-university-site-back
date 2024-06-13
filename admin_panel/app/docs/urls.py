from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "docs"

urlpatterns = [
    path("", login_required(views.DocsList.as_view()), name="docs-list"),
    path("create/", login_required(views.DocsCreate.as_view()), name="docs-create"),
    path("update/<int:pk>/", login_required(views.DocsUpdate.as_view()), name="docs-update"),
    path("delete/<int:pk>/", login_required(views.DocsDelete.as_view()), name="docs-delete"),
    # LawyerPage
    path("lawyer/", login_required(views.LawyerPageList.as_view()), name="lawyer-list"),
    path("lawyer/create/", login_required(views.LawyerPageCreate.as_view()), name="lawyer-create"),
    path("lawyer/update/<int:pk>/", login_required(views.LawyerPageUpdate.as_view()), name="lawyer-update"),
    path("lawyer/delete/<int:pk>/", login_required(views.LawyerPageDelete.as_view()), name="lawyer-delete"),
]
