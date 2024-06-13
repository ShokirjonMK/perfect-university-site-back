from captcha import fields
from django.contrib import admin
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _

from admin_panel.model import courses
from admin_panel.model import docs
from admin_panel.model import event
from admin_panel.model import international
from admin_panel.model import ministry, menu, question, activity
from admin_panel.model import press_service
from admin_panel.model import science
from admin_panel.model import service
from admin_panel.model import settings
from admin_panel.model import static
from admin_panel.model import territorial
from admin_panel.model import useful_link
from admin_panel.model import user
from admin_panel.model import vacancies
from admin_panel.model import contact
from admin_panel.model.scientific import ScientificJournal, ScientificJournalDesc
from django.utils.safestring import mark_safe


class LoginForm(AuthenticationForm):
    captcha = fields.ReCaptchaField()


# admin.site.login_form = LoginForm
# admin.site.login_template = "login.html"

admin.site.register(courses.Admission)
admin.site.register(courses.AdmissionPage)
# international RELATED fields
admin.site.register(international.Grant)
admin.site.register(international.GrantFiles)
admin.site.register(international.InternationalCooperation)
admin.site.register(international.InternationalCooperationCategory)
admin.site.register(international.InternationalPartnerPage)
admin.site.register(international.InternationalPartner)
admin.site.register(international.InternationalConferencePage)
admin.site.register(international.InternationalRelation)
admin.site.register(international.InternationalUsufulLink)
admin.site.register(international.InternationalStaff)
admin.site.register(international.ExternalSection)  # sirtqi bo'lim

# international faculty
admin.site.register(international.InternationalFacultyPage)
admin.site.register(international.InternationalFacultyApplication)

# Science RELATED fields
admin.site.register(science.MonoArticle)
admin.site.register(science.Section)
admin.site.register(science.MonoFiles)
admin.site.register(science.Conference)
admin.site.register(science.ConferenceSubject)
admin.site.register(science.ScienceFiles)
admin.site.register(science.ScienceNews)
admin.site.register(science.ScienceNewsHashtag)
admin.site.register(science.ScienceNewsCategory)
admin.site.register(science.Seminar)
admin.site.register(science.SeminarCategory)
admin.site.register(science.SeminarHashtag)
admin.site.register(settings.TopLink)

# Courses RELATED fields
admin.site.register(courses.CourseCatalog)
admin.site.register(courses.Direction)
admin.site.register(courses.RatingSystem)
admin.site.register(courses.EntrantPage)
admin.site.register(courses.EntrantPageQuestion)
admin.site.register(courses.EntrantPageFile)

# Register your models here.

# Ministry RELATED fields
admin.site.register(ministry.AboutMinistry)
# admin.site.register(ministry.Goal)
# admin.site.register(ministry.Structure)
admin.site.register(ministry.Statistic)
admin.site.register(ministry.StatisticItem)
admin.site.register(ministry.StatisticContentItem)
admin.site.register(ministry.Announcement)
admin.site.register(ministry.StudyProgram)
admin.site.register(ministry.NightProgram)
admin.site.register(ministry.Kafedra)
admin.site.register(ministry.Organization)
admin.site.register(ministry.CouncilStaff)
admin.site.register(ministry.Council)
# admin.site.register(ministry.Camp)
# admin.site.register(ministry.CampImage)
admin.site.register(ministry.FamousGraduate)
admin.site.register(ministry.FamousGraduateGallery)
admin.site.register(ministry.RectorCongratulation)
# admin.site.register(ministry.RegionalDepartment)

# Territorial fields
admin.site.register(territorial.Country)
admin.site.register(territorial.Nationality)
# admin.site.register(territorial.District)

# Settings fields
admin.site.register(settings.MainPageSetting)
admin.site.register(settings.MainPageData)
admin.site.register(settings.Sidebar)
admin.site.register(settings.Typo)
admin.site.register(settings.Slider)

# Docs fields
admin.site.register(docs.Docs)
# Financial report fields
admin.site.register(docs.Report)

# Press service fields
# admin.site.register(press_service.Elonlar)

class GalleryInline(admin.TabularInline):
    model = press_service.Gallery
    extra = 1

@admin.register(press_service.News)
class NewsAdmin(admin.ModelAdmin):
    inlines = [GalleryInline]
    list_display = ("id", "title", 'is_published', 'views', "publish_date", "category")
    list_display_links = ("id", "title")
    search_fields = ("title",)

# admin.site.register(press_service.News)
# admin.site.register(press_service.Gallery)
admin.site.register(press_service.NewsHashtag)
admin.site.register(press_service.NewsCategory)
admin.site.register(press_service.PhotoGallery)
admin.site.register(press_service.PhotoGalleryImage)
admin.site.register(press_service.VideoGallery)
admin.site.register(press_service.FAQ)
admin.site.register(press_service.Objective)

# Service fields
admin.site.register(service.Service)

# Useful link fields
admin.site.register(useful_link.UsefulLink)


# Contact fields
admin.site.register(contact.Contact)
# admin.site.register(contact.UserEmail)

# Static fields

class StaticPagesImageInline(admin.TabularInline):
    model = static.StaticPageImage
    extra = 1


@admin.register(static.StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ("title", "active", "created_at", "updated_at")
    list_filter = ("active",)
    search_fields = ("title",)
    exclude = ("slug",)

    inlines = [StaticPagesImageInline]


# admin.site.register(static.StaticPage)
# admin.site.register(static.StaticPageImage)
# Menu fields
@admin.register(menu.Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ("title", "parent")


# Activity fields
# admin.site.register(activity.Library)
# admin.site.register(activity.LibraryFiles)
# admin.site.register(activity.LibraryCategory)

# admin.site.register(activity.Activity)
admin.site.register(activity.Job)
# admin.site.register(activity.StudentActivityCategory)
# admin.site.register(activity.StudentActivities)
# admin.site.register(activity.Project)
# admin.site.register(activity.Interview)
admin.site.register(activity.Articles)
admin.site.register(activity.Opendata)
admin.site.register(activity.OpenDataFiles)
# admin.site.register(activity.Thesis)


# Quizz fields
# admin.site.register(question.Quizz)
# admin.site.register(question.Question)
# admin.site.register(question.QuestionResult)

# Custom user
admin.site.register(user.CustomUser)

# ExternalImage
# admin.site.register(external.ExternalImage)

# Event
admin.site.register(event.EventsHashtag)
admin.site.register(event.Event)


# VACANCIES ADMIN
class VacancyFieldInlineAdmin(admin.StackedInline):
    model = vacancies.VacancyField
    extra = 0


@admin.register(vacancies.Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "created_at"]
    inlines = (VacancyFieldInlineAdmin,)


class ChoiceFieldOptionsInlineAdmin(admin.StackedInline):
    model = vacancies.ChoiceFieldOptions
    extra = 0


@admin.register(vacancies.VacancyField)
class VacancyFieldAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "field_type"]
    list_filter = ["field_type", "form"]
    inlines = (ChoiceFieldOptionsInlineAdmin,)


@admin.register(vacancies.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]


@admin.register(ScientificJournal)
class ScientificJournalAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    exclude = ("title",)


@admin.register(ScientificJournalDesc)
class ScientificJournalDescAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    exclude = ("title", "description")


class VacantFieldValueInlineAdmin(admin.TabularInline):
    model = vacancies.VacantFieldValue
    extra = 0


@admin.register(vacancies.Vacant)
class VacantAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "created_at", "form"]
    search_fields = ["first_name", "last_name", "middle_name"]
    list_filter = ["form"]
    inlines = (VacantFieldValueInlineAdmin,)


@admin.register(question.Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "surname", "email", "phone_number", "created_at", "updated_at")
    list_display_links = ("id", "name")

    def has_add_permission(self, request):
        return False

    readonly_fields = ("name", "surname", "email", "phone_number", "file", "application_text")


@admin.register(science.ScienceCenter)
class ScienceCenterAdmin(admin.ModelAdmin):
    pass


class DepartmentInfoInline(admin.StackedInline):
    model = ministry.DepartmentInfo
    extra = 0


@admin.register(ministry.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)
    inlines = (DepartmentInfoInline,)


@admin.register(science.PendingConference)
class PendingConferenceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("created_at", "updated_at")
    search_fields = ("title",)


@admin.register(science.ConferenceTags)
class ConferenceTagsAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")
    search_fields = ("name",)


@admin.register(science.ConferenceApplication)
class ConferenceApplicationAdmin(admin.ModelAdmin):
    pass


class OurMissionItemInline(admin.StackedInline):
    model = static.OurMissionItem
    extra = 0


@admin.register(static.OurMission)
class OurMissionAdmin(admin.ModelAdmin):
    inlines = (OurMissionItemInline,)
    list_display = ("id", "title")

    def has_add_permission(self, request):
        if self.model.objects.count() >= 3:
            return False
        return True


class HistoryImageInline(admin.StackedInline):
    model = static.HistoryImage
    extra = 0


class HistoryYearInline(admin.StackedInline):
    model = static.HistoryYear
    extra = 0


class HistoryItemInline(admin.StackedInline):
    model = static.HistoryItem
    extra = 0


@admin.register(static.History)
class HistoryModelAdmin(admin.ModelAdmin):
    inlines = (HistoryImageInline, HistoryYearInline, HistoryItemInline,)
    list_display = ("id", "title", "order")
    list_filter = ("order",)

    def has_add_permission(self, request):
        if self.model.objects.count() >= 2:
            return False
        return True


@admin.register(ministry.ForeignStudent)
class ForeignStudentAdmin(admin.ModelAdmin):
    list_display = ("id", "background_image", "youtube_link")

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return True


@admin.register(international.Ranking)
class RankingModelAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "reputation_ranking", "employer_reputation_ranking")

    def has_add_permission(self, request):
        if self.model.objects.count() > 0:
            return False
        return True


@admin.register(international.JointPrograms)
class JointProgramsModelAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "image", "order")
    list_filter = ("order",)
    search_fields = ("title",)


@admin.register(settings.FAQQuestion)
class FAQQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "order", "created_at", "updated_at")
    list_display_links = ("id", "title")
    search_fields = ("title",)


@admin.register(activity.StudentActivityCategory)
class StudentActivitiesCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'slug')
    list_display_links = ("id", "title", 'slug')
    search_fields = ("title",)
    readonly_fields = ("slug",)


class StudentActivitiesImageInline(admin.TabularInline):
    model = activity.StudentActivityImage
    extra = 1


class StudentActivityContentInline(admin.StackedInline):
    model = activity.StudentActivityContent
    extra = 1


class StudentActivityContentTagInline(admin.StackedInline):
    model = activity.StudentActivityContentTag
    extra = 1


@admin.register(activity.StudentActivityContent)
class StudentActivityContentAdmin(admin.ModelAdmin):
    list_display = ("id", "student_activity", 'title', "content",)
    list_display_links = ("id", 'title', "content")
    search_fields = ("content",)

    inlines = [StudentActivityContentTagInline]


@admin.register(activity.StudentActivities)
class StudentActivitiesAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug", "created_at", "updated_at")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    inlines = [StudentActivitiesImageInline, StudentActivityContentInline]


@admin.register(activity.StudentVideo)
class StudentVideoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "video_url", "created_at")
    search_fields = ("title",)


class StaffGalleryInline(admin.TabularInline):
    model = ministry.StaffGallery
    extra = 1
    verbose_name = _("Staff Gallery")
    verbose_name_plural = _("Staff Galleries")


@admin.register(ministry.Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "position", "phone_number", "image", "order", "rector")
    search_fields = ("title", "position",)
    ordering = ("order",)
    inlines = (StaffGalleryInline,)


@admin.register(ministry.StaffGallery)
class StaffGalleryAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "get_staff",)
    search_fields = ("staff__title",)
    list_select_related = ("staff",)

    def get_staff(self, obj):
        return obj.staff.title

    get_staff.short_description = "Staff Gallery"


class AcademicCalendarFileInline(admin.StackedInline):
    model = activity.AcademicCalendarFile
    extra = 0


@admin.register(activity.AcademicCalendar)
class AcademicCalendarAdmin(admin.ModelAdmin):
    list_display = ("id", "title", 'title_uz', "title_ru", "title_sr", "title_en",)
    list_display_links = ("id", "title",)
    search_fields = ("title",)

    inlines = [AcademicCalendarFileInline]
