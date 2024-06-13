from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "international"

urlpatterns = [
    # Grant
    path("", views.GrantList.as_view(), name="grant-list"),
    path("create/", views.GrantCreate.as_view(), name="grant-create"),
    path("update/<int:pk>/", views.GrantUpdate.as_view(), name="grant-update"),
    path("delete/<int:pk>/", views.GrantDelete.as_view(), name="grant-delete"),
    path("files/delete/<int:pk>/", views.GrantFileDelete.as_view(), name="file-delete"),
    # conferences
    path("conferences-create/", views.InternationalConferencePageCreate.as_view(), name="conference-create"),
    path("conferences-delete/<int:pk>/", views.InternationalConferencePageDelete.as_view(), name="conference-delete"),
    path("conferences-list/", views.InternationalConferencePageList.as_view(), name="conference-list"),
    path("conferences-update/<int:pk>/", views.InternationalConferencePageUpdate.as_view(), name="conference-update"),
    # InternationalRelation
    path("relation/", views.InternationalRelationList.as_view(), name="relation-list"),
    path("relation/create/", views.InternationalRelationCreate.as_view(), name="relation-create"),
    path("relation/update/<int:pk>/", views.InternationalRelationUpdate.as_view(), name="relation-update"),
    path("relation/delete/<int:pk>/", views.InternationalRelationDelete.as_view(), name="relation-delete"),
    # Staff
    path("staff/", views.InternationalStaffList.as_view(), name="staff-list"),
    path("staff/create/", views.InternationalStaffCreate.as_view(), name="staff-create"),
    path("staff/update/<int:pk>/", views.InternationalStaffUpdate.as_view(), name="staff-update"),
    path("staff/delete/<int:pk>/", views.InternationalStaffDelete.as_view(), name="staff-delete"),
    # InternationalUsufulLink
    path("links/", views.InternationalUsufulLinkList.as_view(), name="link-list"),
    path("links/create/", views.InternationalUsufulLinkCreate.as_view(), name="link-create"),
    path("links/update/<int:pk>/", views.InternationalUsufulLinkUpdate.as_view(), name="link-update"),
    path("links/delete/<int:pk>/", views.InternationalUsufulLinkDelete.as_view(), name="link-delete"),
    path("partner-update/", views.InternationalPartnerPageUpdate.as_view(), name="partner-update"),
    path("partners/", login_required(views.InternationalPartnerList.as_view()), name="news-file-list"),
    path("partners/create/", login_required(views.InternationalPartnerCreate.as_view()), name="news-file-create"),
    path(
        "partners/update/<int:pk>/", login_required(views.InternationalPartnerUpdate.as_view()), name="news-file-update"
    ),
    path(
        "partners/delete/<int:pk>/", login_required(views.InternationalPartnerDelete.as_view()), name="news-file-delete"
    ),
    # International Faculty
    path("international-faculty/", views.InternationalFacultyPage.as_view(), name="international-faculty"),
    path(
        "faculty-applications/",
        views.InternationalFacultyApplicationList.as_view(),
        name="international-faculty-application-list",
    ),
    path(
        "faculty-applications/<int:pk>/update/",
        views.InternationalFacultyApplicationUpdate.as_view(),
        name="faculty-application-update",
    ),
    path(
        "faculty-applications/delete/<int:pk>/",
        views.InternationalFacultyApplicationDelete.as_view(),
        name="faculty-application-delete",
    ),
    path(
        "ranking/update/",
        views.RankingUpdate.as_view(),
        name="ranking-update",
    ),
    path(
        "international-category/",
        views.InternationalCooperationCategoryCreate.as_view(),
        name="international-category-create",
    ),
    path(
        "international-category/<int:pk>/update/",
        views.InternationalCooperationCategoryUpdate.as_view(),
        name="international-category-update",
    ),
    path(
        "international-category/delete/<int:pk>/",
        views.InternationalCooperationCategoryDelete.as_view(),
        name="international-category-delete",
    ),
    path(
        "international-category/list/",
        views.InternationalCooperationCategoryList.as_view(),
        name="international-category-list",
    ),
    path(
        "international-cooperation/",
        views.InternationalCooperationCreate.as_view(),
        name="international-cooperation-create",
    ),
    path(
        "international-cooperation/update/<int:pk>/",
        views.InternationalCooperationUpdate.as_view(),
        name="international-cooperation-update",
    ),
    path(
        "international-cooperation/delete/<int:pk>/",
        views.InternationalCooperationDelete.as_view(),
        name="international-cooperation-delete",
    ),
    path(
        "international-cooperation/list/",
        views.InternationalCooperationList.as_view(),
        name="international-cooperation-list",
    ),
]
