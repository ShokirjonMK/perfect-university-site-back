from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from . import forms
from .models import Form, Position, Vacant, NewVacant, Job, JobCategory
from hr import mixins as custom
from django.conf import settings
from .utils import boolen_checker

TRANSFER_HOST = getattr(settings, "TRANSFER_HOST", "example.com")


class VacancyFormCreate(CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    form_class = forms.VacancyForm
    template_name = "back/hr/vacancy_form/create.html"
    success_url = reverse_lazy("vacancy:form-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyFormCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["positions"] = Position.objects.all()
        return context


class VacancyFormList(custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    template_name = "back/hr/vacancy_form/list.html"
    queryset = Form.objects.all()


class VacancyFormUpdate(UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    form_class = forms.VacancyForm
    context_object_name = "object"
    template_name = "back/hr/vacancy_form/update.html"
    success_url = reverse_lazy("vacancy:form-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyFormUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["positions"] = Position.objects.all()
        return context


class VacancyFormDelete(custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    success_url = reverse_lazy("vacancy:form-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        # requests.get(f"{TRANSFER_HOST}/hr/transfer/form-delete/{pk}/")
        return HttpResponseRedirect(self.success_url)


class PositionCreate(custom.CustomCreateView):
    model = Position
    form_class = forms.PositionForm
    template_name = "back/hr/vacancy_form/position_create.html"
    success_url = reverse_lazy("vacancy:position-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("is_published"):
            data["is_published"] = boolen_checker((data.get("is_published")))

        obj = self.model(**data)
        obj.save()
        # data = transfer_serializers.PositionTransferSerializer(obj).data
        # requests.post(f"{TRANSFER_HOST}/hr/transfer/positions-create/", data=data)
        return HttpResponseRedirect(self.success_url)


class PositionUpdate(UpdateView):
    model = Position
    form_class = forms.PositionForm
    context_object_name = "object"
    template_name = "back/hr/vacancy_form/position_update.html"
    success_url = reverse_lazy("vacancy:position-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.save()
        # data = transfer_serializers.PositionTransferSerializer(obj).data
        # requests.put(f"{TRANSFER_HOST}/hr/transfer/positions-update/{obj.id}/", data=data)
        return HttpResponseRedirect(self.success_url)


class PositionList(custom.CustomListView):
    model = Position
    template_name = "back/hr/vacancy_form/position_list.html"
    queryset = Position.objects.all()


class PositionDelete(custom.CustomDeleteView):
    model = Position
    success_url = reverse_lazy("vacancy:position-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        # requests.delete(f"{TRANSFER_HOST}/hr/transfer/positions-delete/{pk}/")
        return HttpResponseRedirect(self.success_url)


class VacantUpdate(UpdateView):
    model = NewVacant
    form_class = forms.VacancyForm
    context_object_name = "object"
    template_name = "back/hr/vacancy_form/position_update.html"
    success_url = reverse_lazy("vacancy:vacant-list")

    def post(self, request, *args, **kwargs):
        # data = request.POST.dict()
        # del data['csrfmiddlewaretoken']
        # obj = self.model.objects.get(id=self.kwargs['pk'])
        # obj.title_uz = data['title_uz']
        # obj.title_ru = data['title_ru']
        # obj.title_en = data['title_en']
        # obj.save()
        return HttpResponseRedirect(self.success_url)


class VacantDetail(DetailView, UpdateView):
    model = NewVacant
    form_class = forms.VacantForm
    context_object_name = "object"
    template_name = "back/hr/vacancy_form/appeal.html"
    success_url = reverse_lazy("vacancy:vacant-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacantDetail, self).get_context_data(object_list=object_list, **kwargs)
        # # context['positions'] = Position.objects.all()
        # context["step2_fields"] = self.object.fields.filter(step=2)
        # context["step3_fields"] = self.object.fields.filter(step=3)
        # context["step4_fields"] = self.object.fields.filter(step=4)
        return context

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            # status = form.cleaned_data.get('status')
            # requests.put(f"{TRANSFER_HOST}/hr/transfer/vacant-status/{self.object.id}/",data={'status':status})
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class VacantList(custom.CustomListView):
    model = NewVacant
    template_name = "back/hr/vacancy_form/appeal_list.html"
    queryset = NewVacant.objects.all()


class VacantDelete(custom.CustomDeleteView):
    model = NewVacant
    success_url = reverse_lazy("vacancy:vacant-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        # requests.delete(f"{TRANSFER_HOST}/hr/transfer/vacant-delete/{pk}/")
        return HttpResponseRedirect(self.success_url)


class JobsCreate(CreateView):
    model = Job
    form_class = forms.LibdaryForm
    template_name = "back/hr/jobs/jobs-create.html"
    success_url = reverse_lazy("vacancy:jobs-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(JobsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["forms"] = Form.objects.all()
        context["categories"] = JobCategory.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False
        if not data["date"]:
            data.pop("date")
        if not data["salary_to"]:
            data["salary_to"] = None
        obj = self.model.objects.create(**data)
        obj.save()
        # data = transfer_serializers.JobTransferSerializer(obj).data
        # requests.post(f"{TRANSFER_HOST}/hr/transfer/job-create/", data=data)
        return HttpResponseRedirect(self.success_url)


class JobsUpdate(UpdateView):
    model = Job
    form_class = forms.LibdaryForm
    context_object_name = "object"
    template_name = "back/hr/jobs/jobs-update.html"
    success_url = reverse_lazy("vacancy:jobs-list")

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
        if not data["salary_to"]:
            data["salary_to"] = None
        obj = self.model.objects.filter(id=int(self.kwargs["pk"]))
        obj.update(**data)
        # data = transfer_serializers.JobTransferSerializer(obj.last()).data
        # requests.put(f"{TRANSFER_HOST}/hr/transfer/job-update/{self.kwargs['pk']}/", data=data)
        return HttpResponseRedirect(self.success_url)


class JobsList(custom.CustomListView):
    model = Job
    template_name = "back/hr/jobs/jobs-list.html"
    queryset = model.objects.all()


class JobsDelete(custom.CustomDeleteView):
    model = Job
    success_url = reverse_lazy("vacancy:jobs-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        # requests.delete(f"{TRANSFER_HOST}/hr/transfer/job-delete/{pk}/")
        return HttpResponseRedirect(self.success_url)
