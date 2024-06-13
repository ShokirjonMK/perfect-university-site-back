from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("", login_required(views.ContactList.as_view()), name="contact-list"),
    # path('create/', login_required(views.DocsCreate.as_view()), name='docs-create'),
    path("update/<int:pk>/", login_required(views.ContactUpdate.as_view()), name="contact-update"),
    path("delete/<int:pk>/", login_required(views.ContactDelete.as_view()), name="contact-delete"),
]
