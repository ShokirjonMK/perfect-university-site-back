from django.contrib.auth.decorators import login_required
from django.urls import path, include

from admin_panel.app.auth.views import Login, Logout, Profile
from admin_panel.app.index.views import Index

# Registering namespace for URL

urlpatterns = [
    # path('api/', include('api.urls')),
    # path('get_image_url/', TinymceImageCreate.as_view(), name='get-image-url'),
    # path('search/', Search.as_view(), name='search'),
    path("", login_required(Index.as_view()), name="index-admin"),
    path("login/", Login.as_view(), name="login"),
    path("logout/", login_required(Logout.as_view()), name="logout"),
    path("profile/", login_required(Profile.as_view()), name="profile"),
    path("about/", include("admin_panel.app.about.urls", namespace="about")),
    path("news/", include("admin_panel.app.news.urls", namespace="news")),
    path("science/", include("admin_panel.app.science.urls", namespace="science")),
    path("courses/", include("admin_panel.app.course.urls", namespace="course")),
    path("admission/", include("admin_panel.app.admission.urls", namespace="admission")),
    path("international/", include("admin_panel.app.international.urls", namespace="international")),
    path("scientific/", include("admin_panel.app.scientific.urls", namespace="scientific")),
    path("gallery/", include("admin_panel.app.gallery.urls", namespace="gallery")),
    path("service/", include("admin_panel.app.service.urls", namespace="service")),
    path("docs/", include("admin_panel.app.docs.urls", namespace="docs")),
    path("reports/", include("admin_panel.app.report.urls", namespace="report")),
    path("event/", include("admin_panel.app.event.urls", namespace="event")),
    path("link/", include("admin_panel.app.link.urls", namespace="link")),
    path("region/", include("admin_panel.app.region.urls", namespace="region")),
    path("quizz/", include("admin_panel.app.quizz.urls", namespace="quizz")),
    path("typo/", include("admin_panel.app.typo.urls", namespace="typo")),
    path("menu/", include("admin_panel.app.menu.urls", namespace="menu")),
    path("static-pages/", include("admin_panel.app.static_page.urls", namespace="static")),
    path("settings/", include("admin_panel.app.settings.urls", namespace="settings")),
    path("user/", include("admin_panel.app.user.urls", namespace="user")),
    path("contact/", include("admin_panel.app.contact.urls", namespace="contact")),
    # path('jobs/', include('admin_panel.app.jobs.urls', namespace='jobs')),
    # path('vacancy-forms/', include('admin_panel.app.vacancy.urls', namespace='vacancy')),
    # path('curricula/', include('admin_panel.app.curricula.urls', namespace='curricula')),
    # path('articles/', include('admin_panel.app.articles.urls', namespace='articles')),
    # path('thesis/', include('admin_panel.app.thesis.urls', namespace='thesis')),
    path("opendata/", include("admin_panel.app.opendata.urls", namespace="opendata")),
    # path('project/', include('admin_panel.app.project.urls', namespace='project')),
    # path('regional_department/', include('admin_panel.app.regional_department.urls',
    # namespace='regional_department')),
]
