from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

# from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.docs import Docs, LawyerPage
from . import forms


class HasRoleMixin:
    pass


# DOCUMENTS
class DocsCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Docs
    form_class = forms.DocsForm
    template_name = "back/docs/doc_create.html"
    success_url = reverse_lazy("docs:docs-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocsCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if not data["date"]:
            del data["date"]

        docs = self.model.objects.create(**data)
        file = request.FILES.get("file")
        if file:
            docs.file = file
        docs.save()
        return HttpResponseRedirect(self.success_url)


class DocsUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Docs
    form_class = forms.DocsForm
    context_object_name = "docs"
    template_name = "back/docs/doc_update.html"
    success_url = reverse_lazy("docs:docs-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DocsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        docs = self.model.objects.get(id=self.kwargs["pk"])

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if not data["date"]:
            del data["date"]

        docs.title_uz = data.get("title_uz")
        docs.title_ru = data.get("title_ru")
        docs.title_en = data.get("title_en")

        docs.law_uz = data.get("law_uz")
        docs.law_ru = data.get("law_ru")
        docs.law_en = data.get("law_en")
        docs.number_uz = data.get("number_uz")
        docs.number_ru = data.get("number_ru")
        docs.number_en = data.get("number_en")

        docs.is_published = data.get("is_published")
        docs.date = data.get("date")
        file = request.FILES.get("file")
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class DocsList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Docs
    template_name = "back/docs/doc_list.html"
    queryset = model.objects.all()


class DocsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Docs
    success_url = reverse_lazy("docs:docs-list")


# LawyerPage
class LawyerPageCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = LawyerPage
    form_class = forms.LawyerPageForm
    template_name = "back/lawyer/doc_create.html"
    success_url = reverse_lazy("docs:lawyer-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LawyerPageCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if not data["date"]:
            del data["date"]

        docs = self.model.objects.create(**data)
        file = request.FILES.get("file")
        if file:
            docs.file = file
        docs.save()
        return HttpResponseRedirect(self.success_url)


class LawyerPageUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = LawyerPage
    form_class = forms.LawyerPageForm
    context_object_name = "docs"
    template_name = "back/lawyer/doc_update.html"
    success_url = reverse_lazy("docs:lawyer-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LawyerPageUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        docs = self.model.objects.get(id=self.kwargs["pk"])

        if not data["date"]:
            del data["date"]

        docs.title_uz = data.get("title_uz")
        docs.title_ru = data.get("title_ru")
        docs.title_en = data.get("title_en")

        docs.date = data.get("date")
        file = request.FILES.get("file")
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class LawyerPageList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = LawyerPage
    template_name = "back/lawyer/doc_list.html"
    queryset = model.objects.all()


class LawyerPageDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = LawyerPage
    success_url = reverse_lazy("docs:lawyer-list")
