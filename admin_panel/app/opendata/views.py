from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView
from django.shortcuts import redirect
from admin_panel.model import activity
from . import forms
from admin_panel.app import views as custom
from django.contrib import messages


class HasRoleMixin:
    pass


class OpendataCreate(CreateView):
    model = activity.Opendata
    form_class = forms.OpendataForm
    template_name = "back/opendata/opendata-create.html"
    success_url = reverse_lazy("opendata:opendata-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OpendataCreate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        try:
            del data["files"]
            if not data.get("url"):
                messages.add_message(request, level=messages.INFO, message="Fayllar yoki sahifa havolasi majburiy")
                return redirect("opendata:opendata-create")
        except KeyError:
            pass
        obj = self.model.objects.create(**data)
        files = request.FILES.getlist("files")
        if files:
            for file in files:
                activity.OpenDataFiles.objects.create(opendata=obj, file=file)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class OpendataUpdate(UpdateView):
    model = activity.Opendata
    form_class = forms.OpendataForm
    context_object_name = "object"
    template_name = "back/opendata/opendata-update.html"
    success_url = reverse_lazy("opendata:opendata-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OpendataUpdate, self).get_context_data(object_list=object_list, **kwargs)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=int(self.kwargs["pk"]))

        files = request.FILES.getlist("files")
        if files:
            for file in files:
                file, _ = activity.OpenDataFiles.objects.get_or_create(opendata=obj, file=file)
        # try:
        #     del data['files']
        #     if not data.get('url'):
        #         messages.add_message(request, messages.INFO, "Fayllar yoki sahifa havolasi majburiy")
        #         return redirect('opendata:opendata-update', pk=int(obj.pk))
        # except KeyError:
        #     pass

        for key, value in data.items():
            if hasattr(obj, key) and value:
                setattr(obj, key, value)
        obj.save()

        return HttpResponseRedirect(self.success_url)


class OpendataList(custom.CustomListView):
    model = activity.Opendata
    template_name = "back/opendata/opendata-list.html"
    queryset = model.objects.all()


class OpendataDelete(custom.CustomDeleteView):
    model = activity.Opendata
    success_url = reverse_lazy("opendata:opendata-list")


class OpendataFileDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = activity.OpenDataFiles
    success_url = reverse_lazy("opendata:opendata-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        # Static page id
        pk = obj.opendata.id
        obj.delete()
        return redirect("opendata:opendata-update", pk=int(pk))
