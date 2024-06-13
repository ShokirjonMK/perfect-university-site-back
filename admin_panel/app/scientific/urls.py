from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "scientific"

urlpatterns = [
    # Scientific-Journal-desc
    path("", login_required(views.ScientificJournalDescList.as_view()), name="scientific-list"),
    path("update/<int:pk>/", login_required(views.ScientificJournalDescUpdate.as_view()), name="scientific-update"),
    # Scientific-Journal
    path("scientific-list/", login_required(views.ScientificJournalList.as_view()), name="scientific_journal-list"),
    path(
        "scientific-create/", login_required(views.ScientificJournalCreate.as_view()), name="scientific_journal-create"
    ),
    path(
        "scientific-update/<int:pk>/",
        login_required(views.ScientificJournalUpdate.as_view()),
        name="scientific_journal-update",
    ),
    path(
        "scientific-delete/<int:pk>/",
        login_required(views.ScientificJournalDelete.as_view()),
        name="scientific_journal-delete",
    ),
]
