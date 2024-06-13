from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from admin_panel.app import views as custom
from . import forms
from ...model.scientific import ScientificJournalDesc, ScientificJournal


class HasRoleMixin:
    pass


class ScientificJournalDescUpdate(HasRoleMixin, custom.CustomUpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournalDesc
    form_class = forms.ScientificJournalDescForm
    template_name = "back/scientific/scientific_journal_update.html"
    success_url = reverse_lazy("scientific:scientific-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        obj.save()

        return HttpResponseRedirect(self.success_url)


class ScientificJournalDescList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournalDesc
    template_name = "back/scientific/scientific_journal_list.html"
    queryset = model.objects.all()
    success_url = reverse_lazy("scientific:scientific-list")


# Scientific Journals


class ScientificJournalList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournal
    template_name = "back/scientific/list.html"
    queryset = model.objects.all()
    success_url = reverse_lazy("scientific:scientific_journal-list")


class ScientificJournalDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournal
    success_url = reverse_lazy("scientific:scientific_journal-list")


class ScientificJournalCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournal
    form_class = forms.ScientificJournalForm
    template_name = "back/scientific/create.html"
    success_url = reverse_lazy("scientific:scientific_journal-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if "image" in data:
            del data["image"]
        if "file" in data:
            del data["file"]

        obj = self.model.objects.create(**data)
        file = request.FILES.get("file")
        image = request.FILES.get("image")
        if file:
            obj.file = file
        if image:
            obj.image = image
        obj.save()
        return HttpResponseRedirect(self.success_url)


class ScientificJournalUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ScientificJournal
    form_class = forms.ScientificJournalForm
    context_object_name = "object"
    template_name = "back/scientific/update.html"
    success_url = reverse_lazy("scientific:scientific_journal-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ScientificJournalUpdate, self).get_context_data(object_list=object_list, **kwargs)
        host = self.request.build_absolute_uri("/")[:-1]
        context["site_url"] = host + "/" + "static/"
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")
        obj.date = data.get("date")
        file = request.FILES.get("file")
        image = request.FILES.get("image")
        if image:
            obj.image = image
        if file:
            obj.file = file
        obj.save()
        return HttpResponseRedirect(self.success_url)
