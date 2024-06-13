# from django.contrib.auth.decorators import login_required
from django.urls import path
from admin_panel.decorators import only_admin as login_required
from . import views

app_name = "settings"
urlpatterns = [
    # path('mainpage/', login_required(views.GeneralSettings.as_view()), name='general'),
    path("mainpage/", login_required(views.MainSettingsView.as_view()), name="general"),
    # Slider
    path("slider/", login_required(views.SliderList.as_view()), name="slider-list"),
    path("slider/create/", login_required(views.SliderCreate.as_view()), name="slider-create"),
    path("slider/update/<int:pk>/", login_required(views.SliderUpdate.as_view()), name="slider-update"),
    path("slider/delete/<int:pk>/", login_required(views.SliderDelete.as_view()), name="slider-delete"),
    # TopLink
    path("top-link/", login_required(views.TopLinkList.as_view()), name="top-link-list"),
    path("top-link/list", login_required(views.TopLinkListApi.as_view()), name="top-link-api"),
    path("top-link/create/", login_required(views.TopLinkCreate.as_view()), name="top-link-create"),
    path("top-link/update/<int:pk>/", login_required(views.TopLinkUpdate.as_view()), name="top-link-update"),
    path("top-link/delete/<int:pk>/", login_required(views.TopLinkDelete.as_view()), name="top-link-delete"),
    # Slider
    path("sidebar/", login_required(views.SidebarList.as_view()), name="sidebar-list"),
    path("sidebar/create/", login_required(views.SidebarCreate.as_view()), name="sidebar-create"),
    path("sidebar/update/<int:pk>/", login_required(views.SidebarUpdate.as_view()), name="sidebar-update"),
    path("sidebar/delete/<int:pk>/", login_required(views.SidebarDelete.as_view()), name="sidebar-delete"),
]
