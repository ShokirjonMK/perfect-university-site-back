from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from .utils import boolen_checker


class CustomCreateView(CreateView):
    model = None
    form_class = None
    template_name = None
    success_url = None

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("is_published"):
            data["is_published"] = boolen_checker((data.get("is_published")))

        obj = self.model(**data)
        obj.save()

        return HttpResponseRedirect(self.success_url)


class CustomUpdateView(UpdateView):
    model = None
    form_class = None
    context_object_name = None
    template_name = None
    success_url = None

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])

        for field, value in data.items():
            if hasattr(obj, field):
                setattr(obj, field, value)
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
