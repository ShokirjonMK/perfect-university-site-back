from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.views import View
from sentry_sdk import capture_exception

from admin_panel.app import views as custom
from admin_panel.model import international, science
from admin_panel.model.user import CustomUser

from . import forms
from ...model.courses import CourseCatalog


class HasRoleMixin:
    pass


class GrantCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.Grant
    form_class = forms.GrantForm
    template_name = "back/international/event_create.html"
    success_url = reverse_lazy("international:grant-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GrantCreate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        # data['region'] = Region.objects.get(id=int(data['region']))

        if not data["publish_date"]:
            del data["publish_date"]
        if "files" in data:
            del data["files"]

        event = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            event.image = image
        files = request.FILES.getlist("files")
        if files:
            for file in files:
                international.GrantFiles.objects.create(grant=event, file=file)

        event.save()

        return HttpResponseRedirect(self.success_url)


class GrantList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.Grant
    template_name = "back/international/event_list.html"
    queryset = model.objects.all()


class GrantUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.Grant
    form_class = forms.GrantForm
    context_object_name = "event"
    template_name = "back/international/event_update.html"
    success_url = reverse_lazy("international:grant-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(GrantUpdate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        event = international.Grant.objects.get(id=self.kwargs["pk"])

        # if not data['start_time']:
        #     del data['start_time']
        if data["publish_date"]:
            event.publish_date = data["publish_date"]

        if data.get("is_published") == "on":
            event.is_published = True
        else:
            event.is_published = False

        # data['region'] = Region.objects.get(id=int(data['region']))

        event.title_uz = data.get("title_uz")
        event.title_ru = data.get("title_ru")
        event.title_en = data.get("title_en")

        event.description_uz = data.get("description_uz")
        event.description_ru = data.get("description_ru")
        event.description_en = data.get("description_en")

        event.short_description_uz = data.get("short_description_uz")
        event.short_description_ru = data.get("short_description_ru")
        event.short_description_en = data.get("short_description_en")

        image = request.FILES.get("image")
        files = request.FILES.getlist("files")
        if image:
            event.image = image
        if files:
            for file in files:
                international.GrantFiles.objects.get_or_create(grant=event, file=file)

        event.save()

        return HttpResponseRedirect(self.success_url)


class GrantDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.Grant
    success_url = reverse_lazy("international:grant-list")


class GrantFileDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.GrantFiles
    success_url = reverse_lazy("international:grant-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        # Static page id
        pk = obj.grant.id
        obj.delete()
        return redirect("international:grant-update", pk=int(pk))


class InternationalConferencePageList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalConferencePage
    template_name = "back/international/conference/conference_list.html"
    queryset = model.objects.all()


class InternationalConferencePageCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalConferencePage
    form_class = forms.InternationalConferencePageForm
    template_name = "back/international/conference/conference_create.html"
    success_url = reverse_lazy("international:conference-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InternationalConferencePageCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["conferences"] = science.ConferenceSubject.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = self.model.objects.create(content_uz=data["content_uz"])
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                print("key", key)
                print("value", value)
                setattr(ministry, key, value)
        ministry.save()
        image = request.FILES.get("image")
        if image:
            ministry.image = image

        ministry.save()

        return HttpResponseRedirect(self.success_url)


class InternationalConferencePageUpdate(HasRoleMixin, custom.CustomUpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalConferencePage
    form_class = forms.InternationalConferencePageForm
    template_name = "back/international/conference/conference.html"
    success_url = reverse_lazy("international:conference-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InternationalConferencePageUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["conferences"] = science.ConferenceSubject.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = international.InternationalConferencePage.objects.get(id=self.kwargs["pk"])
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


class InternationalConferencePageDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalConferencePage
    success_url = reverse_lazy("international:conference-list")


class InternationalConferencePageUpdate1(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("international:conference-update")

    def get(self, request):
        if international.InternationalConferencePage.objects.last():
            page = international.InternationalConferencePage.objects.last()
        else:
            page = international.InternationalConferencePage.objects.create()
        return render(
            request,
            "back/international/conference/conference.html",
            {"object": page, "conferences": science.ConferenceSubject.objects.all()},
        )

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = international.InternationalConferencePage.objects.last()
        hashtags = request.POST.getlist("hashtag")
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

        for hashtag in hashtags:
            print(hashtag)
            try:
                if science.ConferenceSubject.objects.filter(id=int(hashtag)).exists():
                    tag = science.ConferenceSubject.objects.get(id=int(hashtag))
                    if tag not in ministry.conferences.all():
                        ministry.conferences.add(tag)
            except Exception as e:
                capture_exception(e)
                pass

        ministry.save()

        return HttpResponseRedirect(self.success_url)


class InternationalRelationList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalRelation
    template_name = "back/international/relation/list.html"
    queryset = model.objects.all()


class InternationalRelationCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalRelation
    form_class = forms.InternationalRelationForm
    template_name = "back/international/relation/create.html"
    success_url = reverse_lazy("international:relation-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)

        file = request.FILES.get("image")
        if file:
            obj.image = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalRelationUpdate(UpdateView):
    model = international.InternationalRelation
    form_class = forms.InternationalRelationForm
    context_object_name = "object"
    template_name = "back/international/relation/update.html"
    success_url = reverse_lazy("international:relation-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)
        image = request.FILES.get("image")
        if image:
            obj.image = image
        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalRelationDelete(custom.CustomDeleteView):
    model = international.InternationalRelation
    success_url = reverse_lazy("international:relation-list")


# InternationalStaff
class InternationalStaffList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalStaff
    template_name = "back/international/staff/list.html"
    queryset = model.objects.all()


class InternationalStaffCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalStaff
    form_class = forms.InternationalStaffForm
    template_name = "back/international/staff/create.html"
    success_url = reverse_lazy("international:staff-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)

        file = request.FILES.get("image")
        if file:
            obj.image = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalStaffUpdate(UpdateView):
    model = international.InternationalStaff
    form_class = forms.InternationalStaffForm
    context_object_name = "object"
    template_name = "back/international/staff/update.html"
    success_url = reverse_lazy("international:staff-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)
        image = request.FILES.get("image")
        if image:
            obj.image = image
        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalStaffDelete(custom.CustomDeleteView):
    model = international.InternationalStaff
    success_url = reverse_lazy("international:staff-list")


# InternationalUsufulLink
class InternationalUsufulLinkList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalUsufulLink
    template_name = "back/international/usufullink/list.html"
    queryset = model.objects.all()


class InternationalUsufulLinkCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalUsufulLink
    form_class = forms.InternationalUsufulLinkForm
    template_name = "back/international/usufullink/create.html"
    success_url = reverse_lazy("international:link-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalUsufulLinkUpdate(UpdateView):
    model = international.InternationalUsufulLink
    form_class = forms.InternationalUsufulLinkForm
    context_object_name = "object"
    template_name = "back/international/usufullink/update.html"
    success_url = reverse_lazy("international:link-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalUsufulLinkDelete(custom.CustomDeleteView):
    model = international.InternationalUsufulLink
    success_url = reverse_lazy("international:link-list")


class InternationalPartnerPageUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("international:partner-update")

    def get(self, request):
        if international.InternationalPartnerPage.objects.last():
            ministry = international.InternationalPartnerPage.objects.last()
        else:
            ministry = international.InternationalPartnerPage.objects.create()
        return render(request, "back/international/partner/update.html", {"object": ministry})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = international.InternationalPartnerPage.objects.last()
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                setattr(ministry, key, value)
        ministry.save()
        image = request.FILES.get("image")
        if image:
            ministry.image = image
        ministry.save()

        return HttpResponseRedirect(self.success_url)


# files
class InternationalPartnerList(custom.CustomListView):
    model = international.InternationalPartner
    template_name = "back/international/partner/news_files_list.html"
    queryset = model.objects.all()


class InternationalPartnerCreate(CreateView):
    model = international.InternationalPartner
    form_class = forms.InternationalPartnerForm
    template_name = "back/international/partner/news_files_create.html"
    success_url = reverse_lazy("international:news-file-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        docs = self.model.objects.create(**data)
        file = request.FILES.get("file")
        if file:
            docs.image = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class InternationalPartnerUpdate(UpdateView):
    model = international.InternationalPartner
    form_class = forms.InternationalPartnerForm
    context_object_name = "object"
    template_name = "back/international/partner/news_files_update.html"
    success_url = reverse_lazy("international:news-file-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title = data["title"]
        obj.url = data["url"]

        file = request.FILES.get("file")
        if file:
            obj.image = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalPartnerDelete(custom.CustomDeleteView):
    model = international.InternationalPartner
    success_url = reverse_lazy("international:news-file-list")


# International Faculty
class InternationalFacultyPage(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalFacultyPage
    template_name = "back/international/faculty/international_faculty_page.html"
    queryset = model.objects.all()
    success_url = reverse_lazy("international:international-faculty")

    def get(self, request):
        if self.model.objects.first():
            site = self.model.objects.first()
        else:
            site = self.model.objects.create(
                title="International Faculty",
                content="International Faculty",
                video_url="https://www.youtube.com/",
            )
        return render(request, "back/international/faculty/international_faculty_page.html", {"site": site})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        site = self.model.objects.first()
        for key, value in data.items():
            if hasattr(site, key) and value:
                setattr(site, key, value)

        site.save()
        return HttpResponseRedirect(self.success_url)


class InternationalFacultyApplicationList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalFacultyApplication
    template_name = "back/international/faculty/faculty_application_list.html"
    queryset = model.objects.all()


class InternationalFacultyApplicationUpdate(HasRoleMixin, DetailView, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalFacultyApplication
    form_class = forms.InternationalFacultyApplicationForm
    context_object_name = "faculty_application"
    template_name = "back/international/faculty/faculty_application_update.html"
    success_url = reverse_lazy("international:international-faculty-application-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InternationalFacultyApplicationUpdate, self).get_context_data(object_list=object_list, **kwargs)

        degrees = CourseCatalog.objects.all()
        context["degrees"] = degrees
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        appl = international.InternationalFacultyApplication.objects.get(id=self.kwargs["pk"])

        if data.get("is_reviewed") == "on":
            appl.is_reviewed = True
        else:
            appl.is_reviewed = False

        if data.get("is_form_invalid") == "on":
            appl.is_form_invalid = True
        else:
            appl.is_form_invalid = False

        appl.save(update_fields=["is_reviewed", "is_form_invalid"])

        return HttpResponseRedirect(self.success_url)


class InternationalFacultyApplicationDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalFacultyApplication
    success_url = reverse_lazy("international:international-faculty-application-list")


class RankingUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("international:ranking-update")

    def get(self, request):
        if international.Ranking.objects.last():
            page = international.Ranking.objects.last()
        else:
            page = international.Ranking.objects.create()
        return render(request, "back/international/ranking/ranking.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = international.Ranking.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()
        image = request.FILES.get("image")
        if image:
            page.image = image
        page.save()
        return HttpResponseRedirect(self.success_url)


class InternationalCooperationCategoryCreate(custom.CustomCreateView):
    model = international.InternationalCooperationCategory
    form_class = forms.InternationalCooperationCategory
    template_name = "back/international/cooperation/category/category_create.html"
    success_url = reverse_lazy("international:international-category-list")


class InternationalCooperationCategoryUpdate(UpdateView):
    model = international.InternationalCooperationCategory
    form_class = forms.InternationalCooperationCategory
    context_object_name = "object"
    template_name = "back/international/cooperation/category/category_update.html"
    success_url = reverse_lazy("international:international-category-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class InternationalCooperationCategoryList(custom.CustomListView):
    model = international.InternationalCooperationCategory
    template_name = "back/international/cooperation/category/category_list.html"
    queryset = model.objects.all()


class InternationalCooperationCategoryDelete(custom.CustomDeleteView):
    model = international.InternationalCooperationCategory
    success_url = reverse_lazy("international:international-category-list")


class InternationalCooperationCreate(CreateView):
    model = international.InternationalCooperation
    form_class = forms.InternationalCooperationForm
    template_name = "back/international/cooperation/create.html"
    success_url = reverse_lazy("international:international-cooperation-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InternationalCooperationCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["categories"] = international.InternationalCooperationCategory.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("category"):
            data["category"] = international.InternationalCooperationCategory.objects.get(id=int(data["category"]))

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            obj.image = image

        obj.save()

        return HttpResponseRedirect(self.success_url)


class InternationalCooperationUpdate(UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalCooperation
    form_class = forms.InternationalCooperationForm
    context_object_name = "news"
    template_name = "back/international/cooperation/update.html"
    success_url = reverse_lazy("international:international-cooperation-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InternationalCooperationUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["categories"] = international.InternationalCooperationCategory.objects.all()

        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("category"):
            data["category"] = international.InternationalCooperationCategory.objects.get(id=int(data["category"]))

        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.category = data["category"]
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.content_uz = data.get("content_uz")
        obj.content_ru = data.get("content_ru")
        obj.content_en = data.get("content_en")

        image = request.FILES.get("image")
        if image:
            obj.image = image

        obj.save()

        return HttpResponseRedirect(self.success_url)


class InternationalCooperationList(custom.CustomListView):
    model = international.InternationalCooperation
    template_name = "back/international/cooperation/list.html"
    queryset = model.objects.all()


class InternationalCooperationDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = international.InternationalCooperation
    success_url = reverse_lazy("international:international-cooperation-list")
