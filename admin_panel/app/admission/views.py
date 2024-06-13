from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, View

# from rolepermissions.mixins import HasRoleMixin

from admin_panel.app import views as custom
from admin_panel.model import territorial
from . import forms
from admin_panel.model.courses import Admission, Direction, CourseCatalog, AdmissionPage


class HasRoleMixin:
    pass


class AdmissionList(custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Admission
    template_name = "back/admission/list.html"
    queryset = model.objects.all()


class AdmissionCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Admission
    form_class = forms.AdmissionForm
    template_name = "back/admission/create.html"
    success_url = reverse_lazy("admission:admission-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdmissionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["degrees"] = CourseCatalog.objects.all()
        context["applications"] = Direction.objects.all()
        context["countries"] = territorial.Country.objects.all()
        context["nationalities"] = territorial.Nationality.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("errorr_fill") == "on":
            data["errorr_fill"] = True
        else:
            data["errorr_fill"] = False

        if data.get("status") == "on":
            data["status"] = True
        else:
            data["status"] = False

        if data.get("need_dormitory") == "yes":
            data["need_dormitory"] = True
        else:
            data["need_dormitory"] = False

        if data.get("have_higher_education") == "yes":
            data["have_higher_education"] = True
        else:
            data["have_higher_education"] = False

        if data.get("degree"):
            data["degree"] = CourseCatalog.objects.get(pk=int(data.get("degree")))

        if data.get("application"):
            data["application"] = Direction.objects.get(pk=int(data.get("application")))

        if data.get("country"):
            data["country"] = territorial.Country.objects.get(pk=int(data.get("country")))

        if data.get("citizenship"):
            data["citizenship"] = territorial.Country.objects.get(pk=int(data.get("citizenship")))

        if data.get("nationality"):
            data["nationality"] = territorial.Nationality.objects.get(pk=int(data.get("nationality")))

        if data.get("place_of_birth"):
            data["place_of_birth"] = territorial.Country.objects.get(pk=int(data.get("place_of_birth")))

        admission = self.model.objects.create(**data)
        passport_copy = request.FILES.get("passport_copy")

        if passport_copy:
            admission.passport_copy = passport_copy

        photo = request.FILES.get("photo")
        if photo:
            admission.photo = photo

        diploma = request.FILES.get("diploma")
        if diploma:
            admission.diploma = diploma

        admission.save()
        return HttpResponseRedirect(self.success_url)


class AdmissionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Admission
    form_class = forms.AdmissionForm
    template_name = "back/admission/update.html"
    success_url = reverse_lazy("admission:admission-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AdmissionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["degrees"] = CourseCatalog.objects.all()
        context["applications"] = Direction.objects.all()
        context["countries"] = territorial.Country.objects.all()
        context["nationalities"] = territorial.Nationality.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        admission = self.model.objects.get(id=self.kwargs["pk"])
        if data.get("error_fill") == "on":
            admission.error_fill = True
            del data["error_fill"]
        else:
            admission.error_fill = False

        if data.get("status") == "on":
            admission.status = True
            del data["status"]
        else:
            admission.status = False

        if data.get("need_dormitory") == "yes":
            admission.need_dormitory = True
            del data["need_dormitory"]
        else:
            admission.need_dormitory = False

        if data.get("have_higher_education") == "yes":
            admission.have_higher_education = True
            del data["have_higher_education"]
        else:
            admission.have_higher_education = False

        if data.get("degree"):
            data["degree"] = CourseCatalog.objects.get(pk=int(data.get("degree")))

        if data.get("application"):
            data["application"] = Direction.objects.get(pk=int(data.get("application")))

        if data.get("country"):
            data["country"] = territorial.Country.objects.get(pk=int(data.get("country")))

        if data.get("nationality"):
            data["nationality"] = territorial.Nationality.objects.get(pk=int(data.get("nationality")))

        if data.get("place_of_birth"):
            data["place_of_birth"] = territorial.Country.objects.get(pk=int(data.get("place_of_birth")))

        if data.get("citizenship"):
            data["citizenship"] = territorial.Country.objects.get(pk=int(data.get("citizenship")))

        for key, value in data.items():
            if hasattr(admission, key) and value:
                setattr(admission, key, value)

        passport_copy = request.FILES.get("passport_copy")
        if passport_copy:
            admission.passport_copy = passport_copy

        photo = request.FILES.get("photo")
        if photo:
            admission.photo = photo

        diploma = request.FILES.get("diploma")
        if diploma:
            admission.diploma = diploma

        admission.save()

        return HttpResponseRedirect(self.success_url)


class AdmissionDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Admission
    success_url = reverse_lazy("admission:admission-list")


class AdmissionPageUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("admission:admission-page-update")

    def get(self, request):
        if AdmissionPage.objects.last():
            page = AdmissionPage.objects.last()
        else:
            page = AdmissionPage.objects.create()
        return render(request, "back/admission/admission.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = AdmissionPage.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()

        return HttpResponseRedirect(self.success_url)
