from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

# from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model.docs import Report
from . import forms


class HasRoleMixin:
    pass


# REPORTS
class ReportCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Report
    form_class = forms.ReportForm
    template_name = "back/docs/reports/report_create.html"
    success_url = reverse_lazy("report:report-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportCreate, self).get_context_data(object_list=object_list, **kwargs)
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

        report = self.model.objects.create(**data)
        file = request.FILES.get("file")
        if file:
            report.file = file

        report.save()
        return HttpResponseRedirect(self.success_url)


class ReportUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Report
    form_class = forms.ReportForm
    context_object_name = "docs"
    template_name = "back/docs/reports/report_update.html"
    success_url = reverse_lazy("report:report-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ReportUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        report = self.model.objects.get(id=self.kwargs["pk"])

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if not data["date"]:
            del data["date"]

        report.title_uz = data.get("title_uz")
        report.title_ru = data.get("title_ru")
        report.title_en = data.get("title_en")
        report.quarter = data.get("quarter")

        report.is_published = data.get("is_published")
        report.date = data.get("date")
        file = request.FILES.get("file")
        if file:
            report.file = file

        report.save()
        return HttpResponseRedirect(self.success_url)


class ReportList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Report
    template_name = "back/docs/reports/report_list.html"
    queryset = model.objects.all()


class ReportDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Report
    success_url = reverse_lazy("report:report-list")
