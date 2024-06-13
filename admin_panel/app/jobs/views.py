from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

# from rolepermissions.mixins import HasRoleMixin
from admin_panel.model.vacancies import Form
from admin_panel.model import activity
from . import forms
from admin_panel.app import views as custom


class HasRoleMixin:
    pass


class JobsCreate(CreateView):
    model = activity.Job
    form_class = forms.LibdaryForm
    template_name = "back/jobs/jobs-create.html"
    success_url = reverse_lazy("jobs:jobs-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JobsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["forms"] = Form.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        obj = self.model.objects.create(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class JobsUpdate(UpdateView):
    model = activity.Job
    form_class = forms.LibdaryForm
    context_object_name = "object"
    template_name = "back/jobs/jobs-update.html"
    success_url = reverse_lazy("jobs:jobs-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JobsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["forms"] = Form.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False
        obj = self.model.objects.filter(id=int(self.kwargs["pk"]))
        obj.update(**data)
        return HttpResponseRedirect(self.success_url)


class JobsList(custom.CustomListView):
    model = activity.Job
    template_name = "back/jobs/jobs-list.html"
    queryset = model.objects.all()


class JobsDelete(custom.CustomDeleteView):
    model = activity.Job
    success_url = reverse_lazy("jobs:jobs-list")
