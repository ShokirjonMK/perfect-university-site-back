from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from admin_panel.app import views as custom
from admin_panel.model import courses
from admin_panel.model.international import ExternalSection
from admin_panel.model.user import CustomUser
from . import forms


class HasRoleMixin:
    pass


class CourseCatalogList(HasRoleMixin, custom.CustomListView):
    model = courses.CourseCatalog
    allowed_roles = "admin"
    redirect_to_login = "login"
    queryset = model.objects.all()
    template_name = "back/course/list.html"


class CourseCatalogCreate(HasRoleMixin, CreateView):
    model = courses.CourseCatalog
    allowed_roles = "admin"
    redirect_to_login = "login"
    form_class = forms.CourseCatalogForm
    queryset = model.objects.all()
    template_name = "back/course/create.html"
    success_url = reverse_lazy("course:course-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.create(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class CourseCatalogUpdate(HasRoleMixin, UpdateView):
    model = courses.CourseCatalog
    allowed_roles = "admin"
    redirect_to_login = "login"
    form_class = forms.CourseCatalogForm
    queryset = model.objects.all()
    template_name = "back/course/update.html"
    success_url = reverse_lazy("course:course-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class CourseCatalogDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = courses.CourseCatalog
    success_url = reverse_lazy("course:course-list")


# Directions
class DirectionList(custom.CustomListView):
    model = courses.Direction
    template_name = "back/course/directions/list.html"
    queryset = model.objects.all()


class DirectionCreate(CreateView):
    model = courses.Direction
    form_class = forms.DirectionForm
    template_name = "back/course/directions/create.html"
    success_url = reverse_lazy("course:direction-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DirectionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["courses"] = courses.CourseCatalog.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        education_types = courses.EducationType.choices
        context["education_types"] = education_types
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("course"):
            data["course"] = courses.CourseCatalog.objects.get(id=int(data["course"]))
        if data.get("is_admission") == "on":
            data["is_admission"] = True
        else:
            data["is_admission"] = False

        education_types = request.POST.getlist("education_types")
        del data["education_types"]
        data["education_type"] = ",".join(education_types)

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        study_plan = request.FILES.get("study_plan")
        if study_plan:
            obj.study_plan = study_plan

        obj.save()
        return HttpResponseRedirect(self.success_url)


class DirectionUpdate(UpdateView):
    model = courses.Direction
    form_class = forms.DirectionForm
    context_object_name = "news"
    template_name = "back/course/directions/update.html"
    success_url = reverse_lazy("course:direction-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DirectionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["courses"] = courses.CourseCatalog.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        education_types = courses.EducationType.choices
        context["education_types"] = education_types

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("course"):
            data["course"] = courses.CourseCatalog.objects.get(id=int(data["course"]))

        obj = self.model.objects.get(id=self.kwargs["pk"])
        if data.get("is_admission") == "on":
            obj.is_admission = True
            del data["is_admission"]
        else:
            obj.is_admission = False

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)

        study_plan = request.FILES.get("study_plan")
        if study_plan:
            obj.study_plan = study_plan

        education_types = request.POST.getlist("education_types")
        del data["education_types"]
        data["education_types"] = ",".join(education_types)
        obj.education_type = data["education_types"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class DirectionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = courses.Direction
    success_url = reverse_lazy("course:direction-list")


# RatingSystem
class RatingSystemList(custom.CustomListView):
    model = courses.RatingSystem
    template_name = "back/course/rating-system/list.html"
    queryset = model.objects.all()


class RatingSystemCreate(CreateView):
    model = courses.RatingSystem
    form_class = forms.RatingSystemForm
    template_name = "back/course/rating-system/create.html"
    success_url = reverse_lazy("course:rating-system-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RatingSystemCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class RatingSystemUpdate(UpdateView):
    model = courses.RatingSystem
    form_class = forms.RatingSystemForm
    context_object_name = "news"
    template_name = "back/course/rating-system/update.html"
    success_url = reverse_lazy("course:rating-system-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RatingSystemUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class RatingSystemDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = courses.RatingSystem
    success_url = reverse_lazy("course:rating-system-list")


# QualificationRequirements
class QualificationRequirementsList(custom.CustomListView):
    model = courses.QualificationRequirement
    template_name = "back/course/qualification-requirements/list.html"
    queryset = model.objects.all()


class QualificationRequirementsCreate(CreateView):
    model = courses.QualificationRequirement
    form_class = forms.QualificationRequirementsForm
    template_name = "back/course/qualification-requirements/create.html"
    success_url = reverse_lazy("course:qualification-requirements-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QualificationRequirementsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class QualificationRequirementsUpdate(UpdateView):
    model = courses.QualificationRequirement
    form_class = forms.QualificationRequirementsForm
    context_object_name = "news"
    template_name = "back/course/qualification-requirements/update.html"
    success_url = reverse_lazy("course:qualification-requirements-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QualificationRequirementsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class QualificationRequirementsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = courses.QualificationRequirement
    success_url = reverse_lazy("course:qualification-requirements-list")


class CurriculumList(custom.CustomListView):
    model = courses.Curriculum
    template_name = "back/course/curriculum/list.html"
    queryset = model.objects.all()


class CurriculumCreate(CreateView):
    model = courses.Curriculum
    form_class = forms.CurriculumForm
    template_name = "back/course/curriculum/create.html"
    success_url = reverse_lazy("course:curriculum-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CurriculumCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class CurriculumUpdate(UpdateView):
    model = courses.Curriculum
    form_class = forms.CurriculumForm
    context_object_name = "news"
    template_name = "back/course/curriculum/update.html"
    success_url = reverse_lazy("course:curriculum-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CurriculumUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["directions"] = courses.Direction.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("direction"):
            data["direction"] = courses.Direction.objects.get(id=int(data["direction"]))

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class CurriculumDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = courses.Curriculum
    success_url = reverse_lazy("course:curriculum-list")


class EntrantPageList(custom.CustomListView):
    model = courses.EntrantPage
    template_name = "back/course/admission/list.html"
    queryset = model.objects.all()


class EntrantPageCreate(CreateView):
    model = courses.EntrantPage
    form_class = forms.EntrantPageForm
    template_name = "back/course/admission/create.html"
    success_url = reverse_lazy("course:admission-page-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EntrantPageCreate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class EntrantPageDelete(custom.CustomDeleteView):
    model = courses.EntrantPage
    success_url = reverse_lazy("course:admission-page-list")


class EntrantPageUpdate(UpdateView):
    model = courses.EntrantPage
    form_class = forms.EntrantPageForm
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("course:admission-page-list")
    template_name = "back/course/admission/update.html"

    def post(self, request, pk=None):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = self.model.objects.get(id=pk)
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()

        return HttpResponseRedirect(self.success_url)


class EntrantPageFileList(custom.CustomListView):
    model = courses.EntrantPageFile
    template_name = "back/course/admission/file_list.html"
    queryset = model.objects.all()


class EntrantPageFileCreate(CreateView):
    model = courses.EntrantPageFile
    template_name = "back/course/admission/file_create.html"
    form_class = forms.EntrantPageFileForm
    success_url = reverse_lazy("course:admission-file-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EntrantPageFileCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["pages"] = courses.EntrantPage.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        data["entrant_page"] = courses.EntrantPage.objects.get(id=data.get("entrant_page"))

        obj = self.model.objects.create(**data)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class EntrantPageFileUpdate(UpdateView):
    model = courses.EntrantPageFile
    template_name = "back/course/admission/file_update.html"
    form_class = forms.EntrantPageFileForm
    context_object_name = "object"
    success_url = reverse_lazy("course:admission-file-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EntrantPageFileUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["pages"] = courses.EntrantPage.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.entrant_page = courses.EntrantPage.objects.get(id=data.get("entrant_page"))

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class EntrantPageFileDelete(custom.CustomDeleteView):
    model = courses.EntrantPageFile
    success_url = reverse_lazy("course:admission-file-list")


class EntrantPageQuestionList(custom.CustomListView):
    model = courses.EntrantPageQuestion
    template_name = "back/course/admission/question_list.html"
    queryset = model.objects.all()


class EntrantPageQuestionCreate(CreateView):
    model = courses.EntrantPageQuestion
    template_name = "back/course/admission/question_create.html"
    form_class = forms.EntrantPageQuestionForm
    success_url = reverse_lazy("course:admission-question-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EntrantPageQuestionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["pages"] = courses.EntrantPage.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        data["entrant_page"] = courses.EntrantPage.objects.get(id=data.get("entrant_page"))

        obj = self.model.objects.create(**data)

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class EntrantPageQuestionDelete(custom.CustomDeleteView):
    model = courses.EntrantPageQuestion
    success_url = reverse_lazy("course:admission-question-list")


class EntrantPageQuestionUpdate(UpdateView):
    model = courses.EntrantPageQuestion
    template_name = "back/course/admission/question_update.html"
    form_class = forms.EntrantPageQuestionForm
    context_object_name = "object"
    success_url = reverse_lazy("course:admission-question-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(EntrantPageQuestionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["pages"] = courses.EntrantPage.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.entrant_page = courses.EntrantPage.objects.get(id=data.get("entrant_page"))

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.content_uz = data["content_uz"]
        obj.content_ru = data["content_ru"]
        obj.content_en = data["content_en"]
        obj.order = data["order"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


# Sirtqi bo'lim


class ExternalSectionPageList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ExternalSection
    template_name = "back/course/external/external_list.html"
    queryset = model.objects.all()


class ExternalSectionPageCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ExternalSection
    form_class = forms.ExternalSectionPageForm
    template_name = "back/course/external/external_create.html"
    success_url = reverse_lazy("course:external-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExternalSectionPageCreate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = self.model.objects.create(content_uz=data["content_uz"])

        # hashtags = request.POST.getlist("hashtag")
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                print("key", key)
                print("value", value)
                setattr(ministry, key, value)
        ministry.save()
        image = request.FILES.get("image")
        if image:
            ministry.image = image

        # for i in ministry.conferences.all():
        #     ministry.conferences.remove(i)

        # for hashtag in hashtags:
        #     print(hashtag)
        #     try:
        #         if science.ConferenceSubject.objects.filter(
        #                 id=int(hashtag)).exists():
        #             tag = science.ConferenceSubject.objects.get(
        #                 id=int(hashtag))
        #             if tag not in ministry.conferences.all():
        #                 ministry.conferences.add(tag)
        #     except:
        #         pass

        ministry.save()

        return HttpResponseRedirect(self.success_url)


class ExternalSectionPageUpdate(HasRoleMixin, custom.CustomUpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ExternalSection
    form_class = forms.ExternalSectionPageForm
    template_name = "back/course/external/external.html"
    success_url = reverse_lazy("course:external-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExternalSectionPageUpdate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = ExternalSection.objects.get(id=self.kwargs["pk"])
        # hashtags = request.POST.getlist('hashtag')
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                setattr(ministry, key, value)
        ministry.save()
        image = request.FILES.get("image")
        if image:
            ministry.image = image

        # for i in ministry.conferences.all():
        #     ministry.conferences.remove(i)

        # for hashtag in hashtags:
        #     print(hashtag)
        #     try:
        #         if science.ConferenceSubject.objects.filter(
        #                 id=int(hashtag)).exists():
        #             tag = science.ConferenceSubject.objects.get(
        #                 id=int(hashtag))
        #             if tag not in ministry.conferences.all():
        #                 ministry.conferences.add(tag)
        #     except:
        #         pass

        ministry.save()

        return HttpResponseRedirect(self.success_url)


class ExternalSectionPageDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ExternalSection
    success_url = reverse_lazy("course:external-list")
