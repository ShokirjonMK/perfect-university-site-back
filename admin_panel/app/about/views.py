from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView

# from rolepermissions.mixins import HasRoleMixin
from admin_panel.app import views as custom
from admin_panel.app.about import forms
from admin_panel.app.views import CustomCreateView, CustomUpdateView, CustomDeleteView, CustomListView
from admin_panel.model.ministry import (
    AboutMinistry,
    Department,
    Organization,
    Staff,
    Goal,
    Kafedra,
    NightProgram,
    StudyProgram,
)
from admin_panel.model import ministry, question
from django.utils import timezone

from admin_panel.model.static import OurMission, OurMissionItem, History, HistoryImage, HistoryItem, HistoryYear


class HasRoleMixin:
    pass


#
class FamousGraduateCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.FamousGraduate
    form_class = forms.FamousGraduateForm
    template_name = "back/about/famous_graduate_create.html"
    success_url = reverse_lazy("about:famous-graduate-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        # data['is_published'] = boolen_checker(data.get('is_published'))
        # data['main_page'] = boolen_checker(data.get('main_page'))

        obj = self.model.objects.create(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            obj.image = thumbnail

        obj.save()

        images = request.FILES.getlist("image")
        if images:
            for image in images:
                ministry.FamousGraduateGallery.objects.create(famousgraduate=obj, image=image)

        # obj.save()
        return HttpResponseRedirect(self.success_url)


class FamousGraduateList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.FamousGraduate
    form_class = forms.FamousGraduateForm
    queryset = model.objects.all()
    template_name = "back/about/famous_graduate_list.html"


class FamousGraduateUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.FamousGraduate
    form_class = forms.FamousGraduateForm
    context_object_name = "object"
    template_name = "back/about/famous_graduate_update.html"
    success_url = reverse_lazy("about:famous-graduate-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            obj.image = thumbnail

        images = request.FILES.getlist("image")

        if images:
            for image in images:
                image, _ = ministry.FamousGraduateGallery.objects.get_or_create(famousgraduate=obj, image=image)

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.order = data.get("order")

        obj.profession_uz = data.get("profession_uz")
        obj.profession_ru = data.get("profession_ru")
        obj.profession_en = data.get("profession_en")

        obj.faculty_uz = data.get("faculty_uz")
        obj.faculty_ru = data.get("faculty_ru")
        obj.faculty_en = data.get("faculty_en")

        obj.year_uz = data.get("year_uz")
        obj.year_ru = data.get("year_ru")
        obj.year_en = data.get("year_en")

        obj.bio_uz = data.get("bio_uz")
        obj.bio_ru = data.get("bio_ru")
        obj.bio_en = data.get("bio_en")

        obj.tasks_uz = data.get("tasks_uz")
        obj.tasks_ru = data.get("tasks_ru")
        obj.tasks_en = data.get("tasks_en")

        obj.quote_uz = data.get("quote_uz")
        obj.quote_ru = data.get("quote_ru")
        obj.quote_en = data.get("quote_en")
        obj.save()
        return HttpResponseRedirect(self.success_url)


class FamousGraduateDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.FamousGraduate
    success_url = reverse_lazy("about:famous-graduate-list")


class FamousGraduateImageDelete(HasRoleMixin, DeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.FamousGraduateGallery
    success_url = reverse_lazy("about:famous-graduate-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        # Static page id
        pk = obj.famousgraduate.id
        obj.delete()
        return redirect("about:famous-graduate-update", pk=int(pk))


class AboutMinistryUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = AboutMinistry
    success_url = reverse_lazy("about:about-update")

    def get(self, request):
        if AboutMinistry.objects.last():
            ministry = AboutMinistry.objects.last()
        else:
            ministry = AboutMinistry.objects.create()
        return render(request, "back/about/about_ministry.html", {"object": ministry})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = AboutMinistry.objects.last()
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                setattr(ministry, key, value)
        ministry.save()
        image1 = request.FILES.get("image1")
        image2 = request.FILES.get("image2")
        image3 = request.FILES.get("image3")
        if image1:
            ministry.image1 = image1
        file = request.FILES.get("file")
        if file:
            ministry.file = file
        if image2:
            ministry.image2 = image2
        if image3:
            ministry.image3 = image3
        ministry.save()

        return HttpResponseRedirect(self.success_url)


class GoalUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:goal-update")

    def get(self, request):
        if Goal.objects.last():
            obj = Goal.objects.last()
        else:
            obj = Goal.objects.create()
        return render(request, "back/about/goal.html", {"object": obj})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = Goal.objects.last()

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.content_uz = data.get("content_uz")
        obj.content_ru = data.get("content_ru")
        obj.content_en = data.get("content_en")
        obj.save()
        return HttpResponseRedirect(self.success_url)


# Department VIEWS
class DepartmentCreate(HasRoleMixin, CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Department
    form_class = forms.DepartmentForm
    template_name = "back/department/department_update.html"
    success_url = reverse_lazy("about:department-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False
        department = self.model.objects.create(**data)
        image = request.FILES.get("image")
        if image:
            department.image = image
        department.save()
        return HttpResponseRedirect(reverse_lazy("about:department-update", kwargs={"pk": department.id}))


class DepartmentUpdate(CustomUpdateView):
    model = Department
    form_class = forms.DepartmentForm
    context_object_name = "object"
    template_name = "back/department/department_update.html"
    success_url = reverse_lazy("about:department-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        department = Department.objects.get(id=self.kwargs["pk"])
        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            department.main_page = False

        for key, value in data.items():
            if hasattr(department, key) and value:
                setattr(department, key, value)

        image = request.FILES.get("image")
        if image:
            department.image = image
        department.link = data.get("link")
        department.save()

        return HttpResponseRedirect(self.success_url)


class DepartmentList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Department
    template_name = "back/department/department_list.html"
    queryset = model.objects.all()


class DepartmentDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Department
    success_url = reverse_lazy("about:department-list")


# Organization VIEWS
class OrganizationCreate(HasRoleMixin, CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Organization
    form_class = forms.OrganizationForm
    template_name = "back/organization/organization_create.html"
    success_url = reverse_lazy("about:organization-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if "reg_image" in data:
            del data["reg_image"]
        organization = Organization.objects.create(**data)
        reg_image = request.FILES.get("reg_image")
        if reg_image:
            organization.reg_image = reg_image
        organization.save()
        return HttpResponseRedirect(self.success_url)


class OrganizationUpdate(HasRoleMixin, CustomUpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Organization
    form_class = forms.OrganizationForm
    context_object_name = "object"
    template_name = "back/organization/organization_update.html"
    success_url = reverse_lazy("about:organization-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        organization = Organization.objects.get(id=self.kwargs["pk"])
        if "reg_image" in data:
            del data["reg_image"]
        for key, value in data.items():
            if hasattr(organization, key):
                setattr(organization, key, value)
        reg_image = request.FILES.get("reg_image")
        if reg_image:
            organization.reg_image = reg_image
        organization.save()
        return HttpResponseRedirect(self.success_url)


class OrganizationList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Organization
    template_name = "back/organization/organization_list.html"
    queryset = model.objects.all()


class OrganizationDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Organization
    success_url = reverse_lazy("about:organization-list")


# Staff Views


class LeaderCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Staff
    form_class = forms.StaffForm
    template_name = "back/staff/staff_create.html"
    success_url = reverse_lazy("about:staff-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["kafedras"] = Kafedra.objects.all()
        context["faculties"] = Department.objects.all()
        context["organizations"] = Organization.objects.all()
        # if not self.request.user.is_superuser:
        #     context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("kafedra"):
            data["kafedra"] = Kafedra.objects.get(id=int(data["kafedra"]))
        else:
            del data["kafedra"]
        if data.get("department"):
            data["department"] = Department.objects.get(id=int(data["department"]))
        else:
            del data["department"]
        if data.get("organization"):
            data["organization"] = Organization.objects.get(id=int(data["organization"]))
        else:
            del data["organization"]

        if not data["order"]:
            del data["order"]
        if data.get("leader") == "on":
            data["leader"] = True
        else:
            data["leader"] = False
        if data.get("main") == "on":
            data["main"] = True
        else:
            data["main"] = False
        if data.get("rector") == "on":
            data["rector"] = True
        else:
            data["rector"] = False
        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Staff
    form_class = forms.StaffForm
    template_name = "back/staff/staff_update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:staff-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LeaderUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["kafedras"] = Kafedra.objects.all()
        context["faculties"] = Department.objects.all()
        context["organizations"] = Organization.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        if data.get("kafedra"):
            staff.kafedra = Kafedra.objects.get(id=int(data["kafedra"]))
        elif data.get("kafedra") == "":
            staff.kafedra = None
        if data.get("department"):
            staff.department = Department.objects.get(id=int(data["department"]))
        elif data.get("department") == "":
            staff.department = None
        if data.get("organization"):
            staff.organization = Organization.objects.get(id=int(data["organization"]))
        elif data.get("organization") == "":
            staff.organization = None

        # if data.get('main') == 'on':
        #     data['main'] = True
        # else:
        #     data['main'] = False

        if data.get("leader") == "on":
            data["leader"] = True
        else:
            data["leader"] = False
        if data.get("main") == "on":
            data["main"] = True
        else:
            data["main"] = False
        if data.get("rector") == "on":
            data["rector"] = True
        else:
            data["rector"] = False

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.position_uz = data.get("position_uz")
        staff.position_ru = data.get("position_ru")
        staff.position_en = data.get("position_en")
        staff.reception_days_uz = data.get("reception_days_uz")
        staff.reception_days_ru = data.get("reception_days_ru")
        staff.reception_days_en = data.get("reception_days_en")

        staff.duty_uz = data.get("duty_uz")
        staff.duty_ru = data.get("duty_ru")
        staff.duty_en = data.get("duty_en")
        staff.work_history_uz = data.get("work_history_uz")
        staff.work_history_ru = data.get("work_history_ru")
        staff.work_history_en = data.get("work_history_en")

        staff.phone_number = data.get("phone_number")
        staff.email = data.get("email")
        staff.fax = data.get("fax")
        if data.get("order"):
            staff.order = data.get("order")
        else:
            staff.order = None

        # staff.main = data['main']
        staff.leader = data["leader"]
        staff.rector = data["rector"]

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class LeaderList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Staff
    template_name = "back/staff/staff_list.html"
    queryset = model.objects.order_by("-rector", "title", "order")


# Must go to the current url
class LeaderDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Staff
    success_url = reverse_lazy("about:staff-list")


# Council Staffs
class CouncilStaffCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.CouncilStaff
    form_class = forms.CouncilStaffForm
    template_name = "back/about/council-staff/staff_create.html"
    success_url = reverse_lazy("about:council-staff-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CouncilStaffCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class CouncilStaffUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.CouncilStaff
    form_class = forms.CouncilStaffForm
    template_name = "back/about/council-staff/staff_update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:council-staff-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CouncilStaffUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.about_uz = data.get("about_uz")
        staff.about_ru = data.get("about_ru")
        staff.about_en = data.get("about_en")

        staff.order = data.get("order")
        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class CouncilStaffList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.CouncilStaff
    template_name = "back/about/council-staff/staff_list.html"
    queryset = model.objects.all()


# Must go to the current url
class CouncilStaffDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.CouncilStaff
    success_url = reverse_lazy("about:council-staff-list")


class CouncilCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Council
    form_class = forms.CouncilForm
    template_name = "back/about/council/council_create.html"
    success_url = reverse_lazy("about:council-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CouncilCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class CouncilUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Council
    form_class = forms.CouncilForm
    template_name = "back/about/council/council_update.html"
    context_object_name = "council"
    success_url = reverse_lazy("about:council-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CouncilUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.content_uz = data.get("content_uz")
        staff.content_ru = data.get("content_ru")
        staff.content_en = data.get("content_en")

        staff.order = data.get("order")
        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class CouncilList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Council
    template_name = "back/about/council/council_list.html"
    queryset = model.objects.all()


# Must go to the current url
class CouncilDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Council
    success_url = reverse_lazy("about:council-list")


class OurMissionList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMission
    template_name = "back/about/our-mission/our-mission-list.html"
    queryset = model.objects.all()


class OurMissionCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMission
    form_class = forms.OurMissionForm
    template_name = "back/about/our-mission/our-mission-create.html"
    success_url = reverse_lazy("about:our-mission-list")

    def get_context_data(self, **kwargs):
        context = super(OurMissionCreate, self).get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("is_main") == "on":
            data["is_main"] = True
        else:
            data["is_main"] = False

        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class OurMissionUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMission
    form_class = forms.OurMissionForm
    template_name = "back/about/our-mission/our-mission-update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:our-mission-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OurMissionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.description_uz = data.get("description_uz")
        staff.description_ru = data.get("description_ru")
        staff.description_en = data.get("description_en")

        if data.get("is_main") == "on":
            staff.is_main = data["is_main"] = True
        else:
            staff.is_main = data["is_main"] = False

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class OurMissionDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMission
    success_url = reverse_lazy("about:our-mission-list")


class OurMissionItemList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMissionItem
    template_name = "back/about/our-mission_item/mission_item_list.html"
    queryset = model.objects.all()


class OurMissionItemCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMissionItem
    form_class = forms.OurMissionItemForm
    template_name = "back/about/our-mission_item/mission_item_create.html"
    success_url = reverse_lazy("about:our-mission-item-list")

    def get_context_data(self, **kwargs):
        context = super(OurMissionItemCreate, self).get_context_data(**kwargs)
        context["missions"] = OurMission.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        data["our_mission"] = OurMission.objects.get(id=int(data["our_mission"]))
        staff = self.model.objects.create(**data)

        staff.save()

        return HttpResponseRedirect(self.success_url)


class OurMissionItemUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMissionItem
    form_class = forms.OurMissionItemForm
    template_name = "back/about/our-mission_item/mission_item_update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:our-mission-item-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OurMissionItemUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["missions"] = OurMission.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        if data["our_mission"]:
            staff.our_mission = OurMission.objects.get(id=int(data["our_mission"]))
        else:
            del data["our_mission"]

        staff.save()

        return HttpResponseRedirect(self.success_url)


class OurMissionItemDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = OurMissionItem
    success_url = reverse_lazy("about:our-mission-item-list")


class HistoryList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = History
    form_class = forms.HistoryForm
    queryset = model.objects.all()
    template_name = "back/about/history/history_list.html"


class HistoryCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = History
    form_class = forms.HistoryForm
    template_name = "back/about/history/history_create.html"
    success_url = reverse_lazy("about:history-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model(**data)

        obj.save()

        images = request.FILES.getlist("image")
        if images:
            for image in images:
                HistoryImage.objects.create(history=obj, image=image)

        # obj.save()
        return HttpResponseRedirect(self.success_url)


class HistoryDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = History
    success_url = reverse_lazy("about:history-list")


class HistoryUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = History
    form_class = forms.HistoryForm
    context_object_name = "object"
    template_name = "back/about/history/history_update.html"
    success_url = reverse_lazy("about:history-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        images = request.FILES.getlist("image")

        if images:
            for image in images:
                image, _ = HistoryImage.objects.get_or_create(history=obj, image=image)

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.save()
        return HttpResponseRedirect(self.success_url)


class HistoryImageDelete(HasRoleMixin, DeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryImage
    success_url = reverse_lazy("about:history-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        # Static page id
        pk = obj.history.id
        obj.delete()
        return redirect("about:history-update", pk=int(pk))


class HistoryItemList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryItem
    template_name = "back/about/history/history_item/history_item_list.html"
    queryset = model.objects.all()


class HistoryItemCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryItem
    form_class = forms.HistoryItemForm
    template_name = "back/about/history/history_item/history_item_create.html"
    success_url = reverse_lazy("about:history-item-list")

    def get_context_data(self, **kwargs):
        context = super(HistoryItemCreate, self).get_context_data(**kwargs)
        context["histories"] = History.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        data["history"] = History.objects.get(id=int(data["history"]))
        staff = self.model.objects.create(**data)

        staff.save()

        return HttpResponseRedirect(self.success_url)


class HistoryItemUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryItem
    form_class = forms.HistoryItemForm
    template_name = "back/about/history/history_item/history_item_update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:history-item-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HistoryItemUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["histories"] = History.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.content_uz = data["content_uz"]
        staff.content_ru = data["content_ru"]
        staff.content_en = data["content_en"]

        if data["history"]:
            staff.history = History.objects.get(id=int(data["history"]))
        else:
            del data["history"]

        staff.save()

        return HttpResponseRedirect(self.success_url)


class HistoryItemDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryItem
    success_url = reverse_lazy("about:history-item-list")


class HistoryYearList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryYear
    template_name = "back/about/history/history_year/history_year_list.html"
    queryset = model.objects.all()


class HistoryYearCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryYear
    form_class = forms.HistoryYearForm
    template_name = "back/about/history/history_year/history_year_create.html"
    success_url = reverse_lazy("about:history-year-list")

    def get_context_data(self, **kwargs):
        context = super(HistoryYearCreate, self).get_context_data(**kwargs)
        context["histories"] = History.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        data["history"] = History.objects.get(id=int(data["history"]))
        staff = self.model.objects.create(**data)

        staff.save()

        return HttpResponseRedirect(self.success_url)


class HistoryYearUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryYear
    form_class = forms.HistoryYearForm
    template_name = "back/about/history/history_year/history_year_update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:history-year-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HistoryYearUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["histories"] = History.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.description_uz = data["description_uz"]
        staff.description_ru = data["description_ru"]
        staff.description_en = data["description_en"]

        staff.year = data["year"]

        if data["history"]:
            staff.history = History.objects.get(id=int(data["history"]))
        else:
            del data["history"]

        staff.save()

        return HttpResponseRedirect(self.success_url)


class HistoryYearDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = HistoryYear
    success_url = reverse_lazy("about:history-year-list")


class NightProgramUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:sirtqi-update")

    def get(self, request):
        if NightProgram.objects.last():
            ministry = NightProgram.objects.last()
        else:
            ministry = NightProgram.objects.create()
        return render(request, "back/about/night_program.html", {"object": ministry})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        ministry = NightProgram.objects.last()
        for key, value in data.items():
            if hasattr(ministry, key) and value:
                setattr(ministry, key, value)
        ministry.save()

        return HttpResponseRedirect(self.success_url)


# Extra study program
class StudyProgramCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = StudyProgram
    form_class = forms.StudyProgramForm
    template_name = "back/about/study_program/create.html"
    success_url = reverse_lazy("about:program-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudyProgramCreate, self).get_context_data(object_list=object_list, **kwargs)
        # if not self.request.user.is_superuser:
        #     context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False
        if not data["publish_date"]:
            data["publish_date"] = timezone.now()
        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        if image:
            staff.image = image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class StudyProgramUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = StudyProgram
    form_class = forms.StudyProgramForm
    template_name = "back/about/study_program/update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:program-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StudyProgramUpdate, self).get_context_data(object_list=object_list, **kwargs)
        # if not self.request.user.is_superuser:
        #     context['staff'] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]

        staff.description_uz = data.get("description_uz")
        staff.description_ru = data.get("description_ru")
        staff.description_en = data.get("description_en")
        staff.bachelor_uz = data.get("bachelor_uz")
        staff.bachelor_ru = data.get("bachelor_ru")
        staff.bachelor_en = data.get("bachelor_en")

        staff.bachelor_documents_uz = data.get("bachelor_documents_uz")
        staff.bachelor_documents_ru = data.get("bachelor_documents_ru")
        staff.bachelor_documents_en = data.get("bachelor_documents_en")

        staff.master_uz = data.get("master_uz")
        staff.master_ru = data.get("master_ru")
        staff.master_en = data.get("master_en")

        staff.content_uz = data.get("content_uz")
        staff.content_ru = data.get("content_ru")
        staff.content_en = data.get("content_en")
        staff.publish_date = data.get("publish_date")
        if data.get("main_page") == "on":
            staff.main_page = True
        else:
            staff.main_page = False
        image = request.FILES.get("image")
        if image:
            staff.image = image
        staff.link = data.get("link")

        staff.save()

        return HttpResponseRedirect(self.success_url)


class StudyProgramList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = StudyProgram
    template_name = "back/about/study_program/list.html"
    queryset = model.objects.all()


class StudyProgramDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = StudyProgram
    success_url = reverse_lazy("about:program-list")


# Kafedra
class KafedraCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Kafedra
    form_class = forms.KafedraForm
    template_name = "back/department/kafedra/event_create.html"
    success_url = reverse_lazy("about:kafedra-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KafedraCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["faculties"] = Department.objects.all()
        context["staffs"] = Staff.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("faculty"):
            data["faculty"] = Department.objects.get(id=int(data["faculty"]))
        if data.get("mudir") and data.get("mudir") != "":
            data["mudir"] = Staff.objects.get(id=int(data["mudir"]))
        else:
            data["mudir"] = None

        # data['region'] = Region.objects.get(id=int(data['region']))

        event = self.model.objects.create(**data)

        print(data)

        # image = request.FILES.get('image')
        # if image:
        #     event.image = image
        event.save()

        return HttpResponseRedirect(self.success_url)


class KafedraList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Kafedra
    template_name = "back/department/kafedra/event_list.html"
    queryset = model.objects.all()


class KafedraUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Kafedra
    form_class = forms.KafedraForm
    context_object_name = "event"
    template_name = "back/department/kafedra/event_update.html"
    success_url = reverse_lazy("about:kafedra-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(KafedraUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["faculties"] = Department.objects.all()
        context["staffs"] = Staff.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        instance = self.get_object()
        del data["csrfmiddlewaretoken"]
        if data.get("faculty"):
            data["faculty"] = Department.objects.get(id=int(data["faculty"]))
        if data.get("mudir"):
            data["mudir"] = Staff.objects.get(id=int(data["mudir"]))
        elif data.get("mudir") is None or data.get("mudir") == "":
            print(instance.mudir)
            instance.mudir = None
            instance.save()

        event = Kafedra.objects.get(id=self.kwargs["pk"])
        for key, value in data.items():
            if hasattr(event, key) and value:
                setattr(event, key, value)

        event.save()
        return HttpResponseRedirect(self.success_url)


class KafedraDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Kafedra
    success_url = reverse_lazy("about:kafedra-list")


class AnnouncementUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:announcement-update")

    def get(self, request):
        page = ministry.Announcement.objects.last()
        if not page:
            page = ministry.Announcement.objects.create()
        return render(request, "back/about/announcement.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = ministry.Announcement.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()

        return HttpResponseRedirect(self.success_url)


class StatisticPageUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:statistic-update")

    def get(self, request):
        if ministry.Statistic.objects.last():
            page = ministry.Statistic.objects.last()
        else:
            page = ministry.Statistic.objects.create()
        return render(request, "back/about/statistic/statistic.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = ministry.Statistic.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()
        image = request.FILES.get("image")
        icon = request.FILES.get("icon")
        if image:
            page.image = image
        if icon:
            page.icon = icon
        page.save()
        return HttpResponseRedirect(self.success_url)


# StatisticItem
class StatisticItemCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticItem
    form_class = forms.StudyProgramForm
    template_name = "back/about/statistic/create.html"
    success_url = reverse_lazy("about:statisticitem-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StatisticItemCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.create(**data)

        image = request.FILES.get("image")
        blue_image = request.FILES.get("blue_image")
        if image and blue_image:
            staff.image = image
            staff.blue_image = blue_image
        staff.save()

        return HttpResponseRedirect(self.success_url)


class StatisticItemUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticItem
    form_class = forms.StudyProgramForm
    template_name = "back/about/statistic/update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:statisticitem-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StatisticItemUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.title_uz = data["title_uz"]
        staff.title_ru = data["title_ru"]
        staff.title_en = data["title_en"]
        staff.order = data["order"]
        staff.number = data["number"]

        image = request.FILES.get("image")
        blue_image = request.FILES.get("blue_image")
        if image and blue_image:
            staff.image = image
            staff.blue_image = blue_image

        staff.save()

        return HttpResponseRedirect(self.success_url)


class StatisticItemList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticItem
    template_name = "back/about/statistic/list.html"
    queryset = model.objects.all()


class StatisticItemDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticItem
    success_url = reverse_lazy("about:statisticitem-list")


class StatisticContentItemList(HasRoleMixin, CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticContentItem
    template_name = "back/about/statistic_content/list.html"
    queryset = model.objects.all()


class StatisticContentItemCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticContentItem
    form_class = forms.StudyProgramForm
    template_name = "back/about/statistic_content/create.html"
    success_url = reverse_lazy("about:statistic_content_item-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StatisticContentItemCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        self.model.objects.create(**data)

        return HttpResponseRedirect(self.success_url)


class StatisticContentItemUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticContentItem
    form_class = forms.StudyProgramForm
    template_name = "back/about/statistic_content/update.html"
    context_object_name = "staff"
    success_url = reverse_lazy("about:statistic_content_item-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(StatisticContentItemUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        staff = self.model.objects.get(id=self.kwargs["pk"])

        staff.content_uz = data["content_uz"]
        staff.content_ru = data["content_ru"]
        staff.content_en = data["content_en"]
        staff.order = data["order"]

        staff.save()

        return HttpResponseRedirect(self.success_url)


class StatisticContentItemDelete(HasRoleMixin, CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.StatisticContentItem
    success_url = reverse_lazy("about:statistic_content_item-list")


# ForeignStudent
class ForeignStudentUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:foreign-student-update")

    def get(self, request):
        if ministry.ForeignStudent.objects.last():
            page = ministry.ForeignStudent.objects.last()
        else:
            page = ministry.ForeignStudent.objects.create()
        return render(request, "back/about/foreign_student/foreign_student.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = ministry.ForeignStudent.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()
        image = request.FILES.get("background_image")
        if image:
            page.background_image = image
        page.save()
        return HttpResponseRedirect(self.success_url)


class RectorCongratulationUpdate(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    success_url = reverse_lazy("about:rector-update")

    def get(self, request):
        if ministry.RectorCongratulation.objects.last():
            page = ministry.RectorCongratulation.objects.last()
        else:
            page = ministry.RectorCongratulation.objects.create()
        return render(request, "back/about/rectorcongrates.html", {"object": page})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        page = ministry.RectorCongratulation.objects.last()
        for key, value in data.items():
            if hasattr(page, key) and value:
                setattr(page, key, value)
        page.save()
        image = request.FILES.get("image")
        if image:
            page.image = image
        page.save()

        return HttpResponseRedirect(self.success_url)


class ApplicationRectorView(CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = question.Application
    template_name = "back/about/application.html"
    queryset = model.objects.all()


class ApplicationItemDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = question.Application
    success_url = reverse_lazy("about:application")


class ApplicationDetailView(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = question.Application
    template_name = "back/about/application_detail.html"
    # form_class = forms.ContactForm
    success_url = reverse_lazy("about:application")

    def get(self, request, pk):
        context = {
            "application": self.model.objects.get(id=self.kwargs["pk"]),
            "status": question.STATUS,
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        application = self.model.objects.get(id=self.kwargs["pk"])
        application.status = self.request.POST.get("status")
        application.save()
        return HttpResponseRedirect(self.success_url)


# USTAV
class UstavList(HasRoleMixin, custom.CustomListView):
    template_name = "back/settings/ustav/list.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Ustav
    queryset = model.objects.all()


class UstavCreate(HasRoleMixin, custom.CustomCreateView):
    template_name = "back/settings/ustav/create.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Ustav
    form_class = forms.UstavForm
    queryset = model.objects.all()
    success_url = reverse_lazy("about:ustav-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)
        obj.save()
        return HttpResponseRedirect(self.success_url)


class UstavUpdate(HasRoleMixin, custom.CustomUpdateView):
    template_name = "back/settings/ustav/update.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Ustav
    form_class = forms.UstavForm
    queryset = model.objects.all()
    success_url = reverse_lazy("about:ustav-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(pk=self.kwargs.get("pk"))

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.sub_title_uz = data.get("sub_title_uz")
        obj.sub_title_ru = data.get("sub_title_ru")
        obj.sub_title_en = data.get("sub_title_en")

        obj.short_description_uz = data.get("short_description_uz")
        obj.short_description_ru = data.get("short_description_ru")
        obj.short_description_en = data.get("short_description_en")
        obj.order = data.get("order")

        obj.save()
        return HttpResponseRedirect(self.success_url)


class UstavDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.Ustav
    success_url = reverse_lazy("about:ustav-list")


class UstavFileUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = ministry.UnversityFile
    form_class = forms.UnversityFileForm
    context_object_name = "docs"
    template_name = "back/about/ustav-file.html"
    success_url = reverse_lazy("about:ustav-list")

    def get(self, request):
        try:
            ustav = ministry.UnversityFile.objects.get(slug="ustav")
        except ministry.UnversityFile.DoesNotExist:
            ustav = ministry.UnversityFile.objects.create(slug="ustav")
        return render(request, "back/about/ustav-file.html", {"object": ustav})

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        docs = ministry.UnversityFile.objects.get(slug="ustav")

        file = request.FILES.get("file")
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)
