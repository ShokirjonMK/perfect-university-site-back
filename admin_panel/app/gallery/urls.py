from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    # Photogallery urls
    path("photo/", login_required(views.PhotoList.as_view()), name="photo-list"),
    path("photo/create/", login_required(views.PhotoCreate.as_view()), name="photo-create"),
    path("photo/update/<int:pk>/", login_required(views.PhotoUpdate.as_view()), name="photo-update"),
    path("photo/delete/<int:pk>/", login_required(views.PhotoDelete.as_view()), name="photo-delete"),
    path("photo/image/delete/<int:pk>/", login_required(views.PhotoImageDelete.as_view()), name="photo-image-delete"),
    # Videogallery urls
    path("video/", login_required(views.VideoList.as_view()), name="video-list"),
    path("video/create/", login_required(views.VideoCreate.as_view()), name="video-create"),
    path("video/update/<int:pk>/", login_required(views.VideoUpdate.as_view()), name="video-update"),
    path("video/delete/<int:pk>/", login_required(views.VideoDelete.as_view()), name="video-delete"),
    # Vebinar urls
    path("vebinar/", login_required(views.VebinarList.as_view()), name="vebinar-list"),
    path("vebinar/create/", login_required(views.VebinarCreate.as_view()), name="vebinar-create"),
    path("vebinar/update/<int:pk>/", login_required(views.VebinarUpdate.as_view()), name="vebinar-update"),
    path("vebinar/delete/<int:pk>/", login_required(views.VebinarDelete.as_view()), name="vebinar-delete"),
]
