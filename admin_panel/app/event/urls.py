from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "event"

urlpatterns = [
    path("", login_required(views.EventList.as_view()), name="event-list"),
    path("create/", login_required(views.EventCreate.as_view()), name="event-create"),
    path("update/<int:pk>/", login_required(views.EventUpdate.as_view()), name="event-update"),
    path("delete/<int:pk>/", login_required(views.EventDelete.as_view()), name="event-delete"),
    path("hashtags/", login_required(views.EventsHashtagList.as_view()), name="hashtag-list"),
    path("hashtags/create/", login_required(views.EventsHashtagCreate.as_view()), name="hashtag-create"),
    path("hashtags/update/<int:pk>/", login_required(views.EventsHashtagUpdate.as_view()), name="hashtag-update"),
    path("hashtags/delete/<int:pk>/", login_required(views.EventsHashtagDelete.as_view()), name="hashtag-delete"),
]
