from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from admin_panel.app import views as custom
from admin_panel.model.service import Service
from . import forms
from admin_panel.common import boolen_checker


class HasRoleMixin:
    pass


class ServiceCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Service
    form_class = forms.ServiceForm
    template_name = "back/service/service_create.html"
    success_url = reverse_lazy("service:service-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("main_page"):
            data["main_page"] = boolen_checker((data.get("main_page")))

        obj = self.model(**data)
        obj.save()

        if request.FILES.get("icon"):
            obj.icon = request.FILES.get("icon")

        if request.FILES.get("main_icon"):
            obj.main_icon = request.FILES.get("main_icon")

        obj.save()

        return HttpResponseRedirect(self.success_url)


class ServiceUpdate(HasRoleMixin, custom.CustomUpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Service
    form_class = forms.ServiceForm
    template_name = "back/service/service_update.html"
    context_object_name = "service"
    success_url = reverse_lazy("service:service-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if not data.get("main_icon") is None:
            del data["main_icon"]
        if not data.get("icon") is None:
            del data["icon"]
        if data.get("main_page"):
            data["main_page"] = boolen_checker((data.get("main_page")))

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        obj.save()

        if request.FILES.get("main_icon"):
            obj.main_icon = request.FILES.get("main_icon")
        if request.FILES.get("icon"):
            obj.icon = request.FILES.get("icon")

        obj.save()

        return HttpResponseRedirect(self.success_url)


class ServiceList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Service
    template_name = "back/service/service_list.html"
    queryset = model.objects.all()
    success_url = reverse_lazy("service:service-list")


class ServiceDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Service
    success_url = reverse_lazy("service:service-list")
