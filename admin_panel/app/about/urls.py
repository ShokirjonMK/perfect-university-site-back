from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

app_name = "about"

urlpatterns = [
    # path('create/', login_required(views.AboutMinistryCreate.as_view()), name='about-create'),
    path("update/", login_required(views.AboutMinistryUpdate.as_view()), name="about-update"),
    path("announcement/", login_required(views.AnnouncementUpdate.as_view()), name="announcement-update"),
    path("rektor-tabrigi/", login_required(views.RectorCongratulationUpdate.as_view()), name="rector-update"),
    path("rektorga-murojaat/", login_required(views.ApplicationRectorView.as_view()), name="application"),
    path(
        "rektorga-murojaat/delete/<int:pk>/",
        login_required(views.ApplicationItemDelete.as_view()),
        name="applicationitem-delete",
    ),
    path(
        "rektorga-murojaat/update/<int:pk>/",
        login_required(views.ApplicationDetailView.as_view()),
        name="applicationitem-detail",
    ),
    # path('goal/update/', login_required(views.GoalUpdate.as_view()), name='goal-update'),
    # Department
    path("department/", login_required(views.DepartmentList.as_view()), name="department-list"),
    path("department/create/", login_required(views.DepartmentCreate.as_view()), name="department-create"),
    path("department/update/<int:pk>/", login_required(views.DepartmentUpdate.as_view()), name="department-update"),
    path("department/delete/<int:pk>/", login_required(views.DepartmentDelete.as_view()), name="department-delete"),
    # ORganization
    path("organization/", login_required(views.OrganizationList.as_view()), name="organization-list"),
    path("organization/create/", login_required(views.OrganizationCreate.as_view()), name="organization-create"),
    path(
        "organization/update/<int:pk>/", login_required(views.OrganizationUpdate.as_view()), name="organization-update"
    ),
    path(
        "organization/delete/<int:pk>/", login_required(views.OrganizationDelete.as_view()), name="organization-delete"
    ),
    # Staff
    path("staff/", login_required(views.LeaderList.as_view()), name="staff-list"),
    path("staff/create/", login_required(views.LeaderCreate.as_view()), name="staff-create"),
    path("staff/update/<int:pk>/", login_required(views.LeaderUpdate.as_view()), name="staff-update"),
    path("staff/delete/<int:pk>/", login_required(views.LeaderDelete.as_view()), name="staff-delete"),
    # Council Staff
    path("council-staff/", login_required(views.CouncilStaffList.as_view()), name="council-staff-list"),
    path("council-staff/create/", login_required(views.CouncilStaffCreate.as_view()), name="council-staff-create"),
    path(
        "council-staff/update/<int:pk>/",
        login_required(views.CouncilStaffUpdate.as_view()),
        name="council-staff-update",
    ),
    path(
        "council-staff/delete/<int:pk>/",
        login_required(views.CouncilStaffDelete.as_view()),
        name="council-staff-delete",
    ),
    # Council Staff
    path("council/", login_required(views.CouncilList.as_view()), name="council-list"),
    path("council/create/", login_required(views.CouncilCreate.as_view()), name="council-create"),
    path("council/update/<int:pk>/", login_required(views.CouncilUpdate.as_view()), name="council-update"),
    path("council/delete/<int:pk>/", login_required(views.CouncilDelete.as_view()), name="council-delete"),
    # FamousGraduate
    path("famous-graduate/", login_required(views.FamousGraduateList.as_view()), name="famous-graduate-list"),
    path(
        "famous-graduate/create/", login_required(views.FamousGraduateCreate.as_view()), name="famous-graduate-create"
    ),
    path(
        "famous-graduate/update/<int:pk>/",
        login_required(views.FamousGraduateUpdate.as_view()),
        name="famous-graduate-update",
    ),
    path(
        "famous-graduate/delete/<int:pk>/",
        login_required(views.FamousGraduateDelete.as_view()),
        name="famous-graduate-delete",
    ),
    path(
        "image/delete/<int:pk>/",
        login_required(views.FamousGraduateImageDelete.as_view()),
        name="famous-graduate-image-delete",
    ),
    # NightProgram
    path("sirtqi/", login_required(views.NightProgramUpdate.as_view()), name="sirtqi-update"),
    # StudyProgram
    path("program/", login_required(views.StudyProgramList.as_view()), name="program-list"),
    path("program/create/", login_required(views.StudyProgramCreate.as_view()), name="program-create"),
    path("program/update/<int:pk>/", login_required(views.StudyProgramUpdate.as_view()), name="program-update"),
    path("program/delete/<int:pk>/", login_required(views.StudyProgramDelete.as_view()), name="program-delete"),
    # Staff
    path("kafedra/", login_required(views.KafedraList.as_view()), name="kafedra-list"),
    path("kafedra/create/", login_required(views.KafedraCreate.as_view()), name="kafedra-create"),
    path("kafedra/update/<int:pk>/", login_required(views.KafedraUpdate.as_view()), name="kafedra-update"),
    path("kafedra/delete/<int:pk>/", login_required(views.KafedraDelete.as_view()), name="kafedra-delete"),
    # Staff
    path("statistic/", login_required(views.StatisticPageUpdate.as_view()), name="statistic-update"),
    path("statistics/", login_required(views.StatisticItemList.as_view()), name="statisticitem-list"),
    path("statistics/create/", login_required(views.StatisticItemCreate.as_view()), name="statisticitem-create"),
    path(
        "statistics/update/<int:pk>/", login_required(views.StatisticItemUpdate.as_view()), name="statisticitem-update"
    ),
    path(
        "statistics/delete/<int:pk>/", login_required(views.StatisticItemDelete.as_view()), name="statisticitem-delete"
    ),
    path(
        "statistic-content-item/", login_required(views.StatisticContentItemList.as_view()),
        name="statistic_content_item-list"
    ),
    path(
        "statistic-content-item/create/", login_required(views.StatisticContentItemCreate.as_view()),
        name="statistic_content_item-create"
    ),
    path(
        "statistic-content-item/update/<int:pk>/", login_required(views.StatisticContentItemUpdate.as_view()),
        name="statistic_content_item-update"
    ),
    path(
        "statistic-content-item/delete/<int:pk>/", login_required(views.StatisticContentItemDelete.as_view()),
        name="statistic_content_item-delete"
    ),
    path("ustav/", login_required(views.UstavList.as_view()), name="ustav-list"),
    path("ustav/create/", login_required(views.UstavCreate.as_view()), name="ustav-create"),
    path("ustav/update/<int:pk>/", login_required(views.UstavUpdate.as_view()), name="ustav-update"),
    path("ustav/delete/<int:pk>/", login_required(views.UstavDelete.as_view()), name="ustav-delete"),
    path("ustav/file/", login_required(views.UstavFileUpdate.as_view()), name="ustav-file"),

    # OurMission
    path("our-mission/", login_required(views.OurMissionList.as_view()), name="our-mission-list"),
    path("our-mission/create/", login_required(views.OurMissionCreate.as_view()), name="our-mission-create"),
    path("our-mission/update/<int:pk>/", login_required(views.OurMissionUpdate.as_view()), name="our-mission-update"),
    path("our-mission/delete/<int:pk>/", login_required(views.OurMissionDelete.as_view()), name="our-mission-delete"),

    # OurMissionItem
    path("our-mission-item/", login_required(views.OurMissionItemList.as_view()), name="our-mission-item-list"),
    path("our-mission-item/update/<int:pk>/",
         login_required(views.OurMissionItemUpdate.as_view()), name="our-mission-item-update"),
    path("our-mission-item/delete/<int:pk>/",
         login_required(views.OurMissionItemDelete.as_view()), name="our-mission-item-delete"),
    path("our-mission-item/create/",
         login_required(views.OurMissionItemCreate.as_view()), name="our-mission-item-create"),

    # History
    path("history/", login_required(views.HistoryList.as_view()), name="history-list"),
    path("history/create/", login_required(views.HistoryCreate.as_view()), name="history-create"),
    path("history/delete/<int:pk>/", login_required(views.HistoryDelete.as_view()), name="history-delete"),
    path("history/update/<int:pk>/", login_required(views.HistoryUpdate.as_view()), name="history-update"),
    path("history/image/delete/<int:pk>/", login_required(views.HistoryImageDelete.as_view()),
         name="history-image-delete"),
    path("history/item/create/", login_required(views.HistoryItemCreate.as_view()), name="history-item-create"),
    path("history/item/list/", login_required(views.HistoryItemList.as_view()), name="history-item-list"),
    path("history/item/update/<int:pk>/", login_required(views.HistoryItemUpdate.as_view()),
         name="history-item-update"),
    path("history/item/delete/<int:pk>/", login_required(views.HistoryItemDelete.as_view()),
         name="history-item-delete"),
    path("history/year/list/", login_required(views.HistoryYearList.as_view()), name="history-year-list"),
    path("history/year/create/", login_required(views.HistoryYearCreate.as_view()), name="history-year-create"),
    path("history/year/delete/<int:pk>/", login_required(views.HistoryYearDelete.as_view()),
         name="history-year-delete"),
    path("history/year/update/<int:pk>/", login_required(views.HistoryYearUpdate.as_view()),
         name="history-year-update"),

    path("foreign-student/", login_required(views.ForeignStudentUpdate.as_view()), name="foreign-student-update"),
]
