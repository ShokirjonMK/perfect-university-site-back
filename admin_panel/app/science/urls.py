from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "science"

urlpatterns = [
    path("news/", login_required(views.NewsList.as_view()), name="news-list"),
    path("news/create/", login_required(views.NewsCreate.as_view()), name="news-create"),
    path("news/update/<int:pk>/", login_required(views.NewsUpdate.as_view()), name="news-update"),
    path("news/delete/<int:pk>/", login_required(views.NewsDelete.as_view()), name="news-delete"),
    path("science-center/", login_required(views.ScienceCenterView.as_view()), name="science-center-list"),
    path("science-center/create/", login_required(views.ScienceCenterCreate.as_view()), name="science-center-create"),
    path(
        "science-center/update/<int:pk>/",
        login_required(views.ScienceCenterUpdate.as_view()),
        name="science-center-update",
    ),
    path(
        "science-center/delete/<int:pk>/",
        login_required(views.ScienceCenterDelete.as_view()),
        name="science-center-delete",
    ),
    path("category/", login_required(views.NewsCategoryList.as_view()), name="category-list"),
    path("category/create/", login_required(views.NewsCategoryCreate.as_view()), name="category-create"),
    path("category/update/<int:pk>/", login_required(views.NewsCategoryUpdate.as_view()), name="category-update"),
    path("category/delete/<int:pk>/", login_required(views.NewsCategoryDelete.as_view()), name="category-delete"),
    path("hashtag/", login_required(views.NewsHashtagList.as_view()), name="hashtag-list"),
    path("hashtag/create/", login_required(views.NewsHashtagCreate.as_view()), name="hashtag-create"),
    path("hashtag/update/<int:pk>/", login_required(views.NewsHashtagUpdate.as_view()), name="hashtag-update"),
    path("hashtag/delete/<int:pk>/", login_required(views.NewsHashtagDelete.as_view()), name="hashtag-delete"),
    path("files/", login_required(views.NewsFileList.as_view()), name="news-file-list"),
    path("files/create/", login_required(views.NewsFileCreate.as_view()), name="news-file-create"),
    path("files/update/<int:pk>/", login_required(views.NewsFileUpdate.as_view()), name="news-file-update"),
    path("files/delete/<int:pk>/", login_required(views.NewsFileDelete.as_view()), name="news-file-delete"),
    # seminar
    path("seminar/", login_required(views.SeminarList.as_view()), name="seminar-list"),
    path("seminar/create/", login_required(views.SeminarCreate.as_view()), name="seminar-create"),
    path("seminar/update/<int:pk>/", login_required(views.SeminarUpdate.as_view()), name="seminar-update"),
    path("seminar/delete/<int:pk>/", login_required(views.SeminarDelete.as_view()), name="seminar-delete"),
    path("seminar/category/", login_required(views.SeminarCategoryList.as_view()), name="seminar-category-list"),
    path(
        "seminar/category/create/",
        login_required(views.SeminarCategoryCreate.as_view()),
        name="seminar-category-create",
    ),
    path(
        "seminar/category/update/<int:pk>/",
        login_required(views.SeminarCategoryUpdate.as_view()),
        name="seminar-category-update",
    ),
    path(
        "seminar/category/delete/<int:pk>/",
        login_required(views.SeminarCategoryDelete.as_view()),
        name="seminar-category-delete",
    ),
    path("seminar/hashtag/", login_required(views.SeminarHashtagList.as_view()), name="seminar-hashtag-list"),
    path(
        "seminar/hashtag/create/", login_required(views.SeminarHashtagCreate.as_view()), name="seminar-hashtag-create"
    ),
    path(
        "seminar/hashtag/update/<int:pk>/",
        login_required(views.SeminarHashtagUpdate.as_view()),
        name="seminar-hashtag-update",
    ),
    path(
        "seminar/hashtag/delete/<int:pk>/",
        login_required(views.SeminarHashtagDelete.as_view()),
        name="seminar-hashtag-delete",
    ),
    path("article/", login_required(views.MonoArticleList.as_view()), name="article-list"),
    path("article/create/", login_required(views.MonoArticleCreate.as_view()), name="article-create"),
    path("article/update/<int:pk>/", login_required(views.MonoArticleUpdate.as_view()), name="article-update"),
    path("article/delete/<int:pk>/", login_required(views.MonoArticleDelete.as_view()), name="article-delete"),
    # Monografiyalar
    path("monografiya/", login_required(views.MonoSectionList.as_view()), name="mono-list"),
    path("monografiya/create/", login_required(views.MonoSectionCreate.as_view()), name="mono-create"),
    path("monografiya/update/<int:pk>/", login_required(views.MonoSectionUpdate.as_view()), name="mono-update"),
    path("monografiya/delete/<int:pk>/", login_required(views.MonoSectionDelete.as_view()), name="mono-delete"),
    # Seksiyalar
    path("sections/", login_required(views.MonoArticleSectionList.as_view()), name="section-list"),
    path("sections/create/", login_required(views.MonoArticleSectionCreate.as_view()), name="section-create"),
    path("sections/update/<int:pk>/", login_required(views.MonoArticleSectionUpdate.as_view()), name="section-update"),
    path("sections/delete/<int:pk>/", login_required(views.MonoArticleSectionDelete.as_view()), name="section-delete"),
    path(
        "pending-conference/list/",
        login_required(views.PendingConferenceList.as_view()),
        name="pending-conference-list",
    ),
    path(
        "pending-conference/create/",
        login_required(views.PendingConferenceCreate.as_view()),
        name="pending-conference-create",
    ),
    path(
        "pending-conference/update/<int:pk>/",
        login_required(views.PendingConferenceUpdate.as_view()),
        name="pending-conference-update",
    ),
    path(
        "pending-conference/delete/<int:pk>/",
        login_required(views.PendingConferenceDelete.as_view()),
        name="pending-conference-delete",
    ),
    path("conference-tags/", login_required(views.ConferenceTagsList.as_view()), name="conference-tags-list"),
    path(
        "conference-tags/create/", login_required(views.ConferenceTagsCreate.as_view()), name="conference-tags-create"
    ),
    path(
        "conference-tags/update/<int:pk>/",
        login_required(views.ConferenceTagsUpdate.as_view()),
        name="conference-tags-update",
    ),
    path(
        "conference-tags/delete/<int:pk>/",
        login_required(views.ConferenceTagsDelete.as_view()),
        name="conference-tags-delete",
    ),
    path(
        "conference-application/",
        login_required(views.ConferenceApplicationList.as_view()),
        name="conference-application-list",
    ),
    path(
        "conference-application/update/<int:pk>/",
        login_required(views.ConferenceApplicationUpdate.as_view()),
        name="conference-application-update",
    ),
    path(
        "conference-application/delete/<int:pk>/",
        login_required(views.ConferenceApplicationDelete.as_view()),
        name="conference-application-delete",
    ),
    # Conference
    path("conferences/", login_required(views.ConferenceList.as_view()), name="conference-list"),
    path("conferences/create/", login_required(views.ConferenceCreate.as_view()), name="conference-create"),
    path("conferences/update/<int:pk>/", login_required(views.ConferenceUpdate.as_view()), name="conference-update"),
    path("conferences/delete/<int:pk>/", login_required(views.ConferenceDelete.as_view()), name="conference-delete"),
    # Conference Subjects
    path("conference-subject/", login_required(views.ConferenceSubjectList.as_view()), name="conference-subject-list"),
    path(
        "conference-subject/create/",
        login_required(views.ConferenceSubjectCreate.as_view()),
        name="conference-subject-create",
    ),
    path(
        "conference-subject/update/<int:pk>/",
        login_required(views.ConferenceSubjectUpdate.as_view()),
        name="conference-subject-update",
    ),
    path(
        "conference-subject/delete/<int:pk>/",
        login_required(views.ConferenceSubjectDelete.as_view()),
        name="conference-subject-delete",
    ),
]
