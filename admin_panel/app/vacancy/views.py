from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView

# from rolepermissions.mixins import HasRoleMixin
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from . import forms
from admin_panel.model.vacancies import Form, VacancyField, Position, Vacant
from admin_panel.app import views as custom


class HasRoleMixin:
    pass


class VacancyFormCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    form_class = forms.VacancyForm
    template_name = "back/vacancy_form/create.html"
    success_url = reverse_lazy("vacancy:form-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyFormCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["positions"] = Position.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        positions = request.POST.getlist("positions")
        try:
            data.pop("positions")
        except KeyError:
            pass
        del data["csrfmiddlewaretoken"]
        title = data.pop("title")
        object = self.model.objects.create(title=title)

        for position in positions:
            object.positions.add(int(position))

        object.save()
        field_template = "step{}_{}{}"
        step = 2
        row = 0
        while step < 5:
            try:
                title_uz = data[field_template.format(step, "title_uz", row)]
            except KeyError:
                step += 1
                row = 0
                continue
            if data.get(field_template.format(step, "is_published", row)):
                required = True
            else:
                required = False
            field = VacancyField(
                form=object,
                step=int(step),
                title=title_uz,
                title_uz=title_uz,
                title_ru=data.get(field_template.format(step, "title_ru", row)),
                title_en=data.get(field_template.format(step, "title_en", row)),
                placeholder=data.get(field_template.format(step, "placeholder_uz", row)),
                placeholder_uz=data.get(field_template.format(step, "placeholder_uz", row)),
                placeholder_ru=data.get(field_template.format(step, "placeholder_ru", row)),
                placeholder_en=data.get(field_template.format(step, "placeholder_en", row)),
                field_type=int(data.get(field_template.format(step, "field_type", row))),
                required=required,
            )
            field.save()
            row += 1
        return HttpResponseRedirect(self.success_url)


class VacancyFormList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    template_name = "back/vacancy_form/list.html"
    queryset = Form.objects.all()


class VacancyFormUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    form_class = forms.VacancyForm
    context_object_name = "object"
    template_name = "back/vacancy_form/update.html"
    success_url = reverse_lazy("vacancy:form-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacancyFormUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["positions"] = Position.objects.all()
        context["step2_fields"] = self.object.fields.filter(step=2)
        context["step3_fields"] = self.object.fields.filter(step=3)
        context["step4_fields"] = self.object.fields.filter(step=4)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        positions = request.POST.getlist("positions")
        try:
            data.pop("positions")
        except KeyError:
            pass
        title = data.pop("title")
        object = Form.objects.get(id=self.kwargs["pk"])
        object.title = title
        object.positions.clear()
        for position in positions:
            object.positions.add(int(position))
        object.fields.all().delete()
        field_template = "step{}_{}{}"
        step = 2
        row = 0
        while step < 5:
            try:
                title_uz = data[field_template.format(step, "title_uz", row)]
            except KeyError:
                step += 1
                row = 0
                continue
            if data.get(field_template.format(step, "is_published", row)):
                required = True
            else:
                required = False
            field = VacancyField(
                form=object,
                step=int(step),
                title=title_uz,
                title_uz=title_uz,
                title_ru=data.get(field_template.format(step, "title_ru", row)),
                title_en=data.get(field_template.format(step, "title_en", row)),
                placeholder=data.get(field_template.format(step, "placeholder_uz", row)),
                placeholder_uz=data.get(field_template.format(step, "placeholder_uz", row)),
                placeholder_ru=data.get(field_template.format(step, "placeholder_ru", row)),
                placeholder_en=data.get(field_template.format(step, "placeholder_en", row)),
                field_type=int(data.get(field_template.format(step, "field_type", row))),
                required=required,
            )
            field.save()
            row += 1
        object.save()
        return HttpResponseRedirect(self.success_url)


class VacancyFormDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Form
    success_url = reverse_lazy("vacancy:form-list")


class PositionCreate(custom.CustomCreateView):
    model = Position
    form_class = forms.PositionForm
    template_name = "back/vacancy_form/position_create.html"
    success_url = reverse_lazy("vacancy:position-list")


class PositionUpdate(UpdateView):
    model = Position
    form_class = forms.PositionForm
    context_object_name = "object"
    template_name = "back/vacancy_form/position_update.html"
    success_url = reverse_lazy("vacancy:position-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.save()
        return HttpResponseRedirect(self.success_url)


class PositionList(custom.CustomListView):
    model = Position
    template_name = "back/vacancy_form/position_list.html"
    queryset = Position.objects.all()


class PositionDelete(custom.CustomDeleteView):
    model = Position
    success_url = reverse_lazy("vacancy:position-list")


class VacantUpdate(UpdateView):
    model = Vacant
    form_class = forms.VacancyForm
    context_object_name = "object"
    template_name = "back/vacancy_form/position_update.html"
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
    model = Vacant
    form_class = forms.VacantForm
    context_object_name = "object"
    template_name = "back/vacancy_form/appeal.html"
    success_url = reverse_lazy("vacancy:vacant-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacantDetail, self).get_context_data(object_list=object_list, **kwargs)
        # context['positions'] = Position.objects.all()
        context["step2_fields"] = self.object.fields.filter(step=2)
        context["step3_fields"] = self.object.fields.filter(step=3)
        context["step4_fields"] = self.object.fields.filter(step=4)
        return context


class VacantList(custom.CustomListView):
    model = Vacant
    template_name = "back/vacancy_form/appeal_list.html"
    queryset = Vacant.objects.annotate(
        title=Concat("first_name", Value(" "), "last_name", Value(" "), "middle_name", output_field=CharField())
    )


class VacantDelete(custom.CustomDeleteView):
    model = Vacant
    success_url = reverse_lazy("vacancy:vacant-list")
