from django.urls import path

from . import views

app_name = "course"

urlpatterns = [
    # Course catalog
    path("", views.CourseCatalogList.as_view(), name="course-list"),
    path("create/", views.CourseCatalogCreate.as_view(), name="course-create"),
    path("update/<int:pk>/", views.CourseCatalogUpdate.as_view(), name="course-update"),
    path("delete/<int:pk>/", views.CourseCatalogDelete.as_view(), name="course-delete"),
    # Direction catalog
    path("directions/", views.DirectionList.as_view(), name="direction-list"),
    path("directions/create/", views.DirectionCreate.as_view(), name="direction-create"),
    path("directions/update/<int:pk>/", views.DirectionUpdate.as_view(), name="direction-update"),
    path("directions/delete/<int:pk>/", views.DirectionDelete.as_view(), name="direction-delete"),
    # Rating system
    path("rating-system/", views.RatingSystemList.as_view(), name="rating-system-list"),
    path("rating-system/create/", views.RatingSystemCreate.as_view(), name="rating-system-create"),
    path("rating-system/update/<int:pk>/", views.RatingSystemUpdate.as_view(), name="rating-system-update"),
    path("rating-system/delete/<int:pk>/", views.RatingSystemDelete.as_view(), name="rating-system-delete"),
    # Qualification requirements
    path("qualification-requirements/", views.QualificationRequirementsList.as_view(),
         name="qualification-requirements-list"),
    path("qualification-requirements/create/", views.QualificationRequirementsCreate.as_view(),
         name="qualification-requirements-create"),
    path("qualification-requirements/update/<int:pk>/", views.QualificationRequirementsUpdate.as_view(),
         name="qualification-requirements-update"),
    path("qualification-requirements/delete/<int:pk>/", views.QualificationRequirementsDelete.as_view(),
         name="qualification-requirements-delete"),

    # Curriculum
    path("curriculum/", views.CurriculumList.as_view(), name="curriculum-list"),
    path("curriculum/create/", views.CurriculumCreate.as_view(), name="curriculum-create"),
    path("curriculum/update/<int:pk>/", views.CurriculumUpdate.as_view(), name="curriculum-update"),
    path("curriculum/delete/<int:pk>/", views.CurriculumDelete.as_view(), name="curriculum-delete"),

    # admission
    path("admission-page/", views.EntrantPageList.as_view(), name="admission-page-list"),
    path("admission-page/create/", views.EntrantPageCreate.as_view(), name="admission-page-create"),
    path("admission-page/update/<int:pk>/", views.EntrantPageUpdate.as_view(), name="admission-page-update"),
    path("admission-page/delete/<int:pk>/", views.EntrantPageDelete.as_view(), name="admission-page-delete"),
    # admission-file
    path("admission-file/", views.EntrantPageFileList.as_view(), name="admission-file-list"),
    path("admission-file/create/", views.EntrantPageFileCreate.as_view(), name="admission-file-create"),
    path("admission-file/update/<int:pk>/", views.EntrantPageFileUpdate.as_view(), name="admission-file-update"),
    path("admission-file/delete/<int:pk>/", views.EntrantPageFileDelete.as_view(), name="admission-file-delete"),
    # admission-questions
    path("admission-question/", views.EntrantPageQuestionList.as_view(), name="admission-question-list"),
    path("admission-question/create/", views.EntrantPageQuestionCreate.as_view(), name="admission-question-create"),
    path(
        "admission-question/update/<int:pk>/",
        views.EntrantPageQuestionUpdate.as_view(),
        name="admission-question-update",
    ),
    path(
        "admission-question/delete/<int:pk>/",
        views.EntrantPageQuestionDelete.as_view(),
        name="admission-question-delete",
    ),
    # sirtqi bo'lim
    path("external-create/", views.ExternalSectionPageCreate.as_view(), name="external-create"),
    path("external-delete/<int:pk>/", views.ExternalSectionPageDelete.as_view(), name="external-delete"),
    path("external-list/", views.ExternalSectionPageList.as_view(), name="external-list"),
    path("external-update/<int:pk>/", views.ExternalSectionPageUpdate.as_view(), name="external-update"),
]
