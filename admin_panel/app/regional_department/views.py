from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from . import forms
from admin_panel.model.ministry import RegionalDepartment
from admin_panel.app import views as custom


class HasRoleMixin:
    pass


class RegionalDepartmentList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = RegionalDepartment
    template_name = "back/regional_department/regional_department_list.html"
    queryset = model.objects.all()


class RegionalDepartmentUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = RegionalDepartment
    form_class = forms.RegionalDepartmentForm
    context_object_name = "regional_department"
    template_name = "back/regional_department/regional_department_update.html"
    success_url = reverse_lazy("regional_department:regional_department-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        regional_department = RegionalDepartment.objects.get(id=self.kwargs["pk"])

        regional_department.title_uz = data.get("title_uz")
        regional_department.title_ru = data.get("title_ru")
        regional_department.title_en = data.get("title_en")

        regional_department.address_uz = data.get("address_uz")
        regional_department.address_ru = data.get("address_ru")
        regional_department.address_en = data.get("address_en")

        regional_department.director_uz = data.get("director_uz")
        regional_department.director_ru = data.get("director_ru")
        regional_department.director_en = data.get("director_en")

        regional_department.phone_number = data.get("phone_number")
        regional_department.email = data.get("email")

        regional_department.address_url = data.get("address_url")

        regional_department.save()

        return HttpResponseRedirect(self.success_url)


class RegionalDepartmentDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = RegionalDepartment
    success_url = reverse_lazy("regional_department:regional_department-list")
