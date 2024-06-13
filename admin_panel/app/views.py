from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from admin_panel.common import boolen_checker
from admin_panel.model.territorial import Region


class CustomCreateView(CreateView):
    model = None
    form_class = None
    template_name = None
    success_url = None

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super(self.model, self).get_context_data(object_list=object_list, **kwargs)
    #     return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("main_page"):
            data["main_page"] = boolen_checker((data.get("main_page")))
        if data.get("is_published"):
            data["is_published"] = boolen_checker((data.get("is_published")))

        if data.get("scientific_member"):
            """Workers for only Author model"""
            data["scientific_member"] = boolen_checker((data.get("scientific_member")))

        if data.get("region"):
            data["region"] = Region.objects.get(id=int(data["region"]))

        obj = self.model(**data)
        obj.save()

        if request.FILES.get("image"):
            obj.image = request.FILES.get("image")

        if request.FILES.get("icon"):
            obj.icon = request.FILES.get("icon")

        obj.save()

        return HttpResponseRedirect(self.success_url)


class CustomUpdateView(UpdateView):
    model = None
    form_class = None
    context_object_name = None
    template_name = None
    success_url = None

    # def post(self, request, *args, **kwargs):
    #     data = request.POST.dict()
    #     del data['csrfmiddlewaretoken']
    #
    #     obj = self.model.objects.filter(id=self.kwargs['pk'])
    #
    #     obj.update(**data)
    #
    #     for item in obj:
    #         if request.FILES.get('icon'):
    #             item.icon = request.FILES.get('icon')
    #
    #         if request.FILES.get('image'):
    #             item.image = request.FILES.get('image')
    #
    #         item.save()
    #     return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if not data.get("image") is None:
            del data["image"]
        if not data.get("icon") is None:
            del data["icon"]
        if data.get("main_page"):
            data["main_page"] = boolen_checker((data.get("main_page")))

        if data.get("scientific_member") == "on":
            """Workers for only Author model"""
            data["scientific_member"] = boolen_checker((data.get("scientific_member")))
        else:
            data["scientific_member"] = False

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
        obj.save()

        if request.FILES.get("icon"):
            obj.icon = request.FILES.get("icon")

        if request.FILES.get("image"):
            obj.image = request.FILES.get("image")

        obj.save()

        return HttpResponseRedirect(self.success_url)


class CustomListView(ListView):
    model = None
    template_name = None
    queryset = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CustomListView, self).get_context_data(object_list=object_list)
        objects = self.queryset

        q = self.request.GET.get("q")
        if q:
            if hasattr(self.model, "title_uz"):
                if self.request.LANGUAGE_CODE == "en":
                    objects = self.model.objects.filter(title_en__icontains=q)
                if self.request.LANGUAGE_CODE == "ru":
                    objects = self.model.objects.filter(title_ru__icontains=q)
                if self.request.LANGUAGE_CODE == "uz":
                    objects = self.model.objects.filter(title_uz__icontains=q)
            elif hasattr(self.model, "title"):
                objects = self.model.objects.filter(title__icontains=q)

            elif hasattr(self.model, "full_name"):
                objects = self.model.objects.filter(full_name__icontains=q)

        page = self.request.GET.get("page", 1)
        paginator = Paginator(objects, 12)

        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(paginator.num_pages)

        context["objects"] = objects
        return context


class CustomDeleteView(DeleteView):
    model = None
    success_url = None

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        obj.delete()
        return HttpResponseRedirect(self.success_url)
