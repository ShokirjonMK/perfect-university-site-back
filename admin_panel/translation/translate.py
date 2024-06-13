from modeltranslation.translator import TranslationOptions, register

from admin_panel.model import activity
from admin_panel.model import courses
from admin_panel.model import international
from admin_panel.model import science
from admin_panel.model import vacancies
from admin_panel.model.docs import Docs, Report, LawyerPage
from admin_panel.model.event import Event, EventsHashtag
from admin_panel.model.international import ExternalSection, InternationalFacultyPage
from admin_panel.model.menu import Menu
from admin_panel.model.ministry import (
    AboutMinistry,
    Structure,
    Staff,
    Department,
    Organization,
    Goal,
    RegionalDepartment,
    StudyProgram,
    NightProgram,
    Kafedra,
    CouncilStaff,
    StatisticItem,
    Statistic,
    Announcement,
    FamousGraduate,
    RectorCongratulation,
    Ustav,
    DepartmentInfo,
    Council, StatisticContentItem,
)
# ========================Ministry RELATED model========================
from admin_panel.model.press_service import News, PhotoGallery, VideoGallery, FAQ, Vebinar, NewsHashtag, NewsCategory, \
    Objective
from admin_panel.model.question import Quizz, Question
from admin_panel.model.scientific import ScientificJournal, ScientificJournalDesc
from admin_panel.model.service import Service
from admin_panel.model.settings import MainPageSetting, Slider, TopLink, Sidebar, FAQQuestion
from admin_panel.model.static import StaticPage, OurMission, OurMissionItem, History, HistoryYear, HistoryItem, StudentStaticPages
from admin_panel.model.territorial import Region, District, Country, Nationality


class NewsOptions(TranslationOptions):
    fields = ("title", "description")


@register(Objective)
class ObjectiveOptions(TranslationOptions):
    fields = ("title", "description")


class TitleOnlyOption(TranslationOptions):
    fields = ("title",)


@register(international.InternationalConferencePage)
class InternationalConferencePageOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(international.InternationalCooperation)
class InternationalCooperationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(international.JointPrograms)
class JointProgramsOptions(TranslationOptions):
    fields = (
        "title",
    )


@register(international.InternationalCooperationCategory)
class InternationalCooperationCategoryOptions(TranslationOptions):
    fields = (
        "title",
    )


@register(international.InternationalPartnerPage)
class InternationalPartnerPageOptions(TranslationOptions):
    fields = ("content", "title")


@register(RectorCongratulation)
class RectorCongratulationOptions(TranslationOptions):
    fields = ("title", "content", "rector_fullname")


@register(international.InternationalStaff)
class InternationalConferenceItemsOptions(TranslationOptions):
    fields = ("short_description", "place")


@register(international.InternationalRelation)
class InternationalRelationOptions(TranslationOptions):
    fields = (
        "title",
        "short_description",
    )


@register(History)
class HistoryOptions(TranslationOptions):
    fields = ("title", "description")


@register(HistoryYear)
class HistoryYearOptions(TranslationOptions):
    fields = ("title", "description")


@register(HistoryItem)
class HistoryItemOptions(TranslationOptions):
    fields = ("content",)


@register(Statistic)
class StatisticOptions(TranslationOptions):
    fields = ("title", "content", "why_tsue")


@register(Announcement)
class AnnouncementOptions(TranslationOptions):
    fields = ("title", "content")


@register(FamousGraduate)
class FamousGraduateOptions(TranslationOptions):
    fields = ("profession", "faculty", "year", "bio", "tasks", "quote", "title")


@register(StatisticItem)
class StatisticItemOptions(TranslationOptions):
    fields = ("title",)


@register(StatisticContentItem)
class StatisticContentItemOptions(TranslationOptions):
    fields = ("content",)


@register(Country)
class CountryOptions(TranslationOptions):
    fields = ("title",)


@register(Nationality)
class NationalityOptions(TranslationOptions):
    fields = ("title",)


@register(international.Grant)
class GrantOptions(TranslationOptions):
    fields = ("title", "description", "short_description")


@register(science.Seminar)
@register(science.ScienceNews)
class ScienceNewsTranslationOptions(NewsOptions):
    pass


@register(science.SeminarHashtag)
@register(science.ScienceNewsHashtag)
class ScienceNewsHashtagTranslationOptions(TitleOnlyOption):
    pass


@register(science.SeminarCategory)
@register(science.ScienceNewsCategory)
class ScienceNewsCategoryTranslationOptions(TitleOnlyOption):
    pass


@register(science.MonoArticle)
class MonoArticleTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.MonoFiles)
class MonoFilesTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.Conference)
class ConferenceTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.ConferenceSubject)
class ConferenceSubjectTranslationOptions(TranslationOptions):
    fields = ("title", "department", "place")


@register(science.ScienceFiles)
class ScienceFilesTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.PendingConference)
class PendingConferenceTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(science.ConferenceTags)
class ConferenceTagsTranslationOptions(TranslationOptions):
    fields = ("name",)


@register(courses.CourseCatalog)
class CourseCatalogTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(courses.AdmissionPage)
class AdmissionPageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(courses.Direction)
class DirectionTranslationOptions(TranslationOptions):
    fields = ("title", "qualification", "content")


@register(courses.EntrantPage)
class EntrantPageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(courses.EntrantPageQuestion)
class EntrantPageQuestionTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(courses.EntrantPageFile)
class EntrantPageFileTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(AboutMinistry)
class AboutMinistryTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(Goal)
class GoalTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(Structure)
class StructureTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(StudyProgram)
class StudyProgramTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
        "bachelor",
        "bachelor_documents",
        "master",
        "content",
    )


@register(Staff)
class StaffTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "position",
        "reception_days",
        "work_history",
        "duty",
        'bio',
        'task',
    )

@register(activity.StudentVideo)
class StudentVideoTranslationOptions(TranslationOptions):
    fields = (
        "title",
    )

@register(activity.StudentActivityContent)
class StudentActivityContentTranslationOptions(TranslationOptions):
    fields = (
        'title',
        "content",
    )

@register(activity.StudentActivityContentTag)
class StudentActivityContentTagTranslationOptions(TranslationOptions):
    fields = (
        'tag',
    )

@register(Department)
class DepartmentTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "kafedras",
        "directions",
        "history",
        "study_works",
        "spiritual_directions",
        "research_works",
        "innovative_works",
        "faculty_innovative_works",
        "cooperation",
        "international_relations",
        "description",
        "faculty_international_relations",
    )


@register(DepartmentInfo)
class DepartmentInfoTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(Organization)
class OrganizationTranslationOptions(TranslationOptions):
    fields = ("title", "content", "reg_subtitle", "reg_title")


@register(CouncilStaff)
class CouncilStaffTranslation(TranslationOptions):
    fields = ("about", "title")


@register(Council)
class CouncilTranslation(TranslationOptions):
    fields = ("title", "content")


# Territorial fields
@register(Region)
class RegionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(District)
class DistrictTranslationOptions(TranslationOptions):
    fields = ("title",)


# Settings fields
@register(MainPageSetting)
class MainPageSettingTranslationOptions(TranslationOptions):
    fields = ("title", "address", "logo", "logo_white", "footer_content", "quote", "quote_author")


# Slider fields
@register(Slider)
class SliderTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "image")


# Docs fields
@register(Docs)
class DocsTranslationOptions(TranslationOptions):
    fields = ("title", "law", "number")


@register(LawyerPage)
class LawyerPageTranslationOptions(TranslationOptions):
    fields = ("title",)


# Financial report
@register(Report)
class ReportTranslationOptions(TranslationOptions):
    fields = ("title",)


# Press service fields
@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ("title", "short_description", "description")


# @register(Elonlar)
# class ElonlarTranslationOptions(TranslationOptions):
#     fields = (
#         'title', 'description',
#     )


@register(NewsHashtag)
class NewsHashtagTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(NewsCategory)
class NewsCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(PhotoGallery)
class PhotoGalleryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(VideoGallery)
class VideoGalleryTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(Vebinar)
class VebinarTranslationOptions(TranslationOptions):
    fields = ("title", "author")


#
# @register(Camp)
# class CampTranslationOptions(TranslationOptions):
#     fields = (
#         'content',
#     )


@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "author",
    )


# Service fields
@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


# Static fields
@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )

@register(StudentStaticPages)
class StudentStaticPagesTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "content",
    )


@register(OurMission)
class OurMissionOptions(TranslationOptions):
    fields = (
        "title",
        "description"
    )


@register(OurMissionItem)
class OurMissionItemOptions(TranslationOptions):
    fields = (
        "title",
    )


# Event tag fields
@register(EventsHashtag)
class EventHashtagTranslationOptions(TranslationOptions):
    fields = ("title",)


# Event fields
@register(Event)
class EventTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


# Menu fields
@register(Menu)
class MenuTranslationOptions(TranslationOptions):
    fields = ("title", "description")


# Quizz fields
@register(Quizz)
class QuizzTranslationOptions(TranslationOptions):
    fields = ("title",)


# Quizz fields
@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(activity.Articles)
class ArticlesTranslationOptions(TranslationOptions):
    fields = ("title", "author", "content")


@register(activity.StudentActivities)
class StudentActivitiesTranslationOptions(TranslationOptions):
    fields = ("title", "content")

@register(activity.StudentActivityCategory)
class StudentActivitiesCategoryTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(activity.AcademicCalendar)
class AcademicCalendarTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(RegionalDepartment)
class RegionalDepartmentTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "address",
        "director",
    )


@register(activity.Opendata)
class OpendataTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(NightProgram)
class NightProgramTranslationOptions(TranslationOptions):
    fields = ("title", "address", "content", "goals_tasks", "tasks", "bachelor", "directions")


@register(Kafedra)
class KafedraTranslationOptions(TranslationOptions):
    fields = ("title", "about", "content")


# @register(activity.Opendata)
# class OpendataTranslationOptions(TranslationOptions):
#     fields = (
#         'title','url'
#     )


@register(activity.Job)
class JobTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "department",
        "content",
    )


@register(TopLink)
class TopLinkTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(Sidebar)
class SidebarTranslationOptions(TranslationOptions):
    fields = ("title", "button_title")


@register(Ustav)
class UstavTranslationOptions(TranslationOptions):
    fields = ("title", "sub_title", "short_description")


@register(vacancies.ChoiceFieldOptions)
class ChoiceFieldOptionsTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(vacancies.VacancyField)
class VacancyFieldTranslationOptions(TranslationOptions):
    fields = ("title", "placeholder")


@register(vacancies.Position)
class PositionTranslationOptions(TranslationOptions):
    fields = ("title",)


@register(science.ScienceCenter)
class ScienceCenterTranslationOptions(TranslationOptions):
    fields = ("title", "description", "reception_time")


@register(ScientificJournal)
class ScientificJournalTranslationOptions(TranslationOptions):
    fields = ("title", "description")


@register(ScientificJournalDesc)
class ScientificJournalDescTranslationOptions(TranslationOptions):
    fields = (
        "title",
        "description",
    )


# Sirtqi bo'lim
@register(ExternalSection)
class ExternalSectionTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(InternationalFacultyPage)
class InternationalFacultyPageTranslationOptions(TranslationOptions):
    fields = ("title", "content")


@register(FAQQuestion)
class FAQQuestionTranslationOptions(TranslationOptions):
    fields = ("title", "content", )