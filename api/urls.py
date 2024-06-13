from django.urls import path, include
from rest_framework import routers
from rest_framework_nested import routers as nested_route
from api.our_mission import views as our_mission
from api.about import views as about
from api.activity import views as activity
from api.admission import views as admission
from api.contact import views as contact
from api.courses import views as courses_catalog
from api.courses.views import QualificationRequirementsViewSet
from api.foreign_student import views as st
from api.docs import views as docs
from api.event import views as event
from api.gallery import views as gallery
from api.international import views as international
from api.news import views as news
from api.quizz import views as quizz
from api.science import views as science
from api.search import views as search
from api.service import views as service
from api.settings import views as site
from api.static import views as static
from api.typo import views as typo
from api.auth import views as auth
from api.history import views as history
from api.team import views as team
from . import views
from .scientific.views import ScientificJournalDescListApiView, ScientificJournalListApiView
from .settings.views import MainPageDataView
from .staff_excel import ImportExcelStaff
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
nested_router = nested_route.SimpleRouter()
# router.register(r'index', index.IndexViewSet, basename='index-api')


router.register("admission", admission.AdmissionCreate, basename="admission-api")

# Settings
router.register(r"site-contact", site.SiteContactView, basename="site-contact-api")
router.register(r"site", site.SiteContactView, basename="site-api")
router.register(r"rekvizit", site.RekvizitView, basename="rekvizit-api")
router.register(r"slider", site.SliderView, basename="slider-api")
router.register(r"sidebar", site.SidebarViewSet, basename="sidebar-api")
# Index
router.register(r"header", site.HeaderView, basename="header-api")
router.register(r"footer", site.FooterView, basename="footer-api")
router.register(r"statistic", about.StatisticView, basename="statistic-api")
router.register(r"announcement", about.AnnouncementView, basename="announcement-api")
router.register(r"top-news", news.IndexNewsListView, basename="top-news-api")
# router.register(r'top-elonlar', news.IndexElonlarListView,
#                 basename='top-elonlar-api')


# router.register(r'top-opendata', activity.IndexOpendataListView,
#                 basename='top-opendata-api')
router.register(r"top-faculty", about.DepartmentMainPageView, basename="top-faculty-api")
router.register(r"top-vebinar", gallery.TopVebinarView, basename="top-vebinar-api")
# router.register(r'top-photo', gallery.TopPhotoView, basename='top-photo-api')
router.register(r"top-event", event.TopEventView, basename="top-event-api")
router.register(r"ustav", about.UstavViewSet, basename="ustav-api")
router.register(r"catalog-file", about.UnversityCatalogSet, basename="course-file-api")

# Science
router.register("mono-article", science.MonoArticleViewSet, basename="mono-article-api")
router.register("conferences", science.ConferenceViewSet, basename="conferences-api")
router.register("conferences-year", science.ConferenceYearsView, basename="conferences-api")
router.register("science-files", science.ScienceFilesViewSet, basename="science-files-api")
router.register("science-news", science.ScienceNewsViewSet, basename="science-news-api")
router.register("science-seminar", science.SeminarViewSet, basename="science-seminar-api")

# international
router.register("international-grant", international.InternationalViewSet, basename="international-grant-api")
router.register(
    "international-relations", international.InternationalRelationView, basename="international-relations-api"
)
router.register(
    "international-scholarship", international.InternationalPartnerPageView, basename="international-scholarship-api"
)
router.register(
    "international-conferences",
    international.InternationalConferencePageViewSet,
    basename="international-conferences-api",
)

# Course Catalog
router.register("course-rating-system", courses_catalog.RatingSystemViewSet, basename="rating-system-api")
router.register("qualification-requirements", QualificationRequirementsViewSet,
                basename="qualification-requirements-api")
router.register("curriculum", courses_catalog.CurriculumViewSet, basename="curriculum-api")
router.register("course-entrant-page", courses_catalog.EntrantPage, basename="entrant-page-api")

router.register("international-admission-page", courses_catalog.AdmissionPageView, basename="admission-page-api")

# Nested routers
# course
nested_router.register("course", courses_catalog.CourseCatalogViewSet, basename="course-api")
course_router = nested_route.NestedSimpleRouter(nested_router, r"course", lookup="course")
course_router.register(r"direction", courses_catalog.DirectionViewSet, basename="courese-direction")

# Famous graduates

nested_router.register("famous-graduate", about.FamousGraduateViewSet, basename="famous-graduate-api")
famous_graduate_gallery_router = nested_route.NestedSimpleRouter(
    nested_router, r"famous-graduate", lookup="famousgraduate"
)
famous_graduate_gallery_router.register(
    r"gallery", about.FamousGraduateGalleryViewSet, basename="famous_graduate_gallery"
)

# Famous Main graduates

nested_router.register("famous-graduate-index", about.FamousGraduateMainViewSet, basename="famous-graduate-index-api")
# router.register(r'course-catalog', courses_catalog.CourseCatalogViewSet,
#                 basename='course-catalog-api')
# router.register(r'direction', courses_catalog.DirectionViewSet,
#                 basename='direction-api')

# All staff and leaders
router.register(r"leader", about.StaffView, basename="leader-api")

# Press API
router.register(r"news", news.NewsListView, basename="news-api")
# router.register(r'elonlar', news.ElonlarListView, basename='elonlar-api')

# Useful links
router.register(r"partners", site.PartnersView, basename="partner-api")

# Gallery
router.register(r"photo", gallery.PhotoListView, basename="photo-api")
router.register(r"video", gallery.VideoListView, basename="video-api")
router.register(r"vebinar", gallery.VebinarListView, basename="vebinar-api")

# Event
router.register(r"event", event.EventListView, basename="event-api")

# Quizz
router.register(r"quizz", quizz.QuizzListView, basename="quizz-api")

# Articles
# router.register(r'articles', activity.ArticlesListView,
#                 basename='articles-api')


# Open data
router.register(r"opendata", activity.OpendataListView, basename="opendata-api")

# About us page
router.register(r"about", about.AboutUsView, basename="about-api")
router.register(r"rector", about.RectorCongratulationView, basename="rector-api")
router.register(r"goal", about.GoalView, basename="goal-api")
router.register(r"structure", about.StructureView, basename="structure-api")

# router.register(r'news-category', news.NewsCategoryView, basename='news-category-api')
# router.register(r'news-hashtag', news.NewsHashtagView, basename='news-hashtag-api')
router.register(r"quote", news.FAQListView, basename="faq-legal-api")
# router.register(r'faq-psychologic', news.FAQPsychologicView, basename='faq-psychologic-api')
# router.register(r'faq-teen', news.FAQTeenView, basename='faq-teen-api')
# router.register(r'faq-female', news.FAQFemaleView, basename='faq-female-api')


router.register(r"typo", typo.TypoView, basename="typo-api")

# Static page
router.register(r"static", static.StaticView, basename="static-api")

# Docs
router.register(r"docs", docs.DocsListView, basename="docs-api")
# financial Report
router.register(r"report", docs.ReportListView, basename="report-api")
router.register(r"lawyer", docs.LawyerPageView, basename="lawyer-api")
# Job
router.register(r"job", activity.JobListView, basename="job-api")

router.register(r"job-category", activity.JobCategoryList, basename="job-category-api")

# Contact
router.register(r"contact", contact.ContactView, basename="contact-api")

# Region
router.register(r"region", site.RegionView, basename="region-api")

# Region
router.register(r"email", contact.Email, basename="email-api")

router.register(r"faculty", about.DepartmentView, basename="faculty-api")
router.register(r"kafedra", about.KafedraView, basename="kafedra-api")
router.register(r"centers", about.OrganizationView, basename="centers-api")
router.register(r"scientifics", about.CouncilStaffListViewSet, basename="scientific-council-api")

# router.register(r'camp', about.CampListViewSet,
#                 basename='camp-api')

router.register(r"extra-programs", about.StudyProgramView, basename="extra-programs-api")
router.register(r"top-extra-programs", about.TopStudyProgramView, basename="top-extra-programs-api")
router.register(r"night-program", about.NightProgramView, basename="night-programs-api")
router.register(r"regional_department", site.RegionalDepartmentView, basename="regional_department-api")

router.register(r"scientific_journal", ScientificJournalDescListApiView, basename="scientific-journals-api")
router.register(r"scientific_journal-desc", ScientificJournalListApiView, basename="scientific-journals-desc-api")
router.register(r"service", service.ServiceTopListView, basename="top-service-api")
router.register(r"service-list", service.ServiceListView, basename="service-api")
# router.register(r'top-quizz', quizz.QuizzView, basename='top-quiz-api')

# router.register(r'top-activity', activity.TopActivityListView, basename='top-activity-api')

# router.register(r'poster', site.PosterView, basename='poster-api')

urlpatterns = [
    path("student-activities/", activity.StudentActivitiesListAPIView.as_view(), name="student-activities-api"),
    path("student-activities/<slug:slug>/", activity.StudentActivityRetreviewAPIView.as_view()),
    path("student-activity-category/", activity.StudentActivityCategoryListAPIView.as_view()),
    path("student/videos/", activity.StudentVideoListAPIView.as_view(), name="student-videos-api"),

    path("academic-calendars/", activity.AcademicCalendarListAPIView.as_view(), name="academic-calendar-api"),
    # Maqsadlar listi
    path("our-mission/", our_mission.OurMissionListAPIView.as_view(), name="our-mission-api"),
    path("history/", history.HistoryListAPIView.as_view(), name="history-api"),
    path("objectives/", news.ObjectiveListView.as_view(), name="objectives-api"),
    path("objectives/<str:slug>/", news.ObjectiveDetailView.as_view(), name="objectives-detail-api"),

    path("science-center/", science.ScienceCenterListView.as_view()),
    path("science-center/<slug:slug>/", science.ScienceCenterSingleView.as_view()),
    path("news-category/", news.NewsCategoryView.as_view()),
    path("faculty/<int:department_id>/infos/", about.DepartmentInfoListCreateView.as_view()),
    path("faculty/infos/<int:pk>/", about.DepartmentInfoRetrieveUpdateDestroyAPIView.as_view()),
    path("application/", quizz.ApplicationView.as_view()),
    path("admission/objects/", admission.admission_objects, name="admission-objects-api"),
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
    path("", include(course_router.urls)),
    path("", include(famous_graduate_gallery_router.urls)),
    path("search/", search.Search.as_view(), name="search-api"),
    path("lawyer-views/<int:pk>/", docs.counter, name="lawyer-counter-api"),
    path("menu/<str:slug>/", views.MenuRetrieveView.as_view(), name="menu-retrieve"),
    path("image-upload/", site.ImageUploadView.as_view(), name="image-upload"),
    path("council/", about.CouncilListView.as_view(), name="council-list-api"),
    path("council/<int:pk>", about.CouncilDetailView.as_view(), name="council-list-api-detail"),
    path("staff/<int:pk>", about.DepartmentStaffView.as_view(), name="staffs-retrieve-api-detail"),
    # sirtqi bo'lim
    path("external-section/", international.ExternalSectionListView.as_view(), name="external-section-api"),
    path(
        "external-section/<int:pk>",
        international.ExternalSectionDetailView.as_view(),
        name="external-section-detail-api",
    ),
    path("excel_staff/", ImportExcelStaff.as_view(), name="excel-staff-api"),
    path("conference/list/", science.ConferenceListView.as_view(), name="conference-list-api"),
    path("conference/<int:pk>/detail/", science.ConferenceDetailView.as_view(), name="conference-detail-api"),
    path("conference/application/", science.ConferenceApplicationCreateView.as_view(), name="conference-register-api"),
    # international faculty
    path(
        "international-faculty-page/",
        international.InternationalFacultyPageDetailAPIView.as_view(),
        name="international-faculty-page-detail-api",
    ),
    path(
        "international-faculty-application/create/",
        international.InternationalFacultyApplicationCreateAPIView.as_view(),
        name="international-faculty-application-create-api",
    ),
    path(
        "international-cooperation/",
        international.InternationalCooperationListAPIView.as_view(),
        name="international-cooperation-list-api",
    ),
    path(
        "international-ranking/",
        international.RankingListAPIView.as_view(),
        name="international-ranking-list-api",

    ),
    path(
        "international-joint-programs/",
        international.JointProgramListAPIView.as_view(),
        name="international-joint-programs-list-api",
    ),
    path(
        "foreign-student/list/",
        st.ForeignStudentListAPIView.as_view(),
        name="foreign-student-list-api"
    ),
    # AUTH
    path(
        "auth/profile/",
        auth.UserProfileView.as_view(),
        name="profile-api"
    ),
    path(
        "auth/register/",
        auth.UserRegisterView.as_view(),
        name="register-api"
    ),
    path(
        "auth/login/",
        auth.UserLoginView.as_view(),
        name="login-api"
    ),
    path(
        "auth/login/refresh/",
        TokenRefreshView.as_view(),
        name="refresh-token-api"
    ),
    path(
        "auth/update-profile/",
        auth.UserUpdateProfileView.as_view(),
        name="update-profile-api"
    ),
    path(
        "auth/send-verification-code/",
        auth.SendVerificationCodeAPIView.as_view(),
        name="send-verification-code-api"
    ),
    path(
        "auth/verify-reset-code/",
        auth.VerifyResetPasswordCodeAPIView.as_view(),
        name="verify-reset-code-api"
    ),
    path(
        "auth/reset-password/",
        auth.ResetPasswordAPIView.as_view(),
        name="reset-password-api"
    ),
    path("MainPageData/", MainPageDataView.as_view(), name="main-page-data"),
    path("faq-questions/", about.FAQQuestionListView.as_view(), name="faq-questions"),
    path("team-members/", team.TeamListApiView.as_view(), name="team-members"),
    path("team-members/<int:pk>/", team.TeamMemberDetailApiView.as_view(), name="team-members-detail"),
]


