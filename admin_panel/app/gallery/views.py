from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect
from . import forms
from admin_panel.model.press_service import PhotoGallery, PhotoGalleryImage, VideoGallery, Vebinar
from admin_panel.app import views as custom
from admin_panel.common import boolen_checker


class HasRoleMixin:
    pass


class PhotoCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = PhotoGallery
    form_class = forms.PhotoForm
    template_name = "back/press_service/photo_gallery_create.html"
    success_url = reverse_lazy("gallery:photo-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if not data["publish_date"]:
            del data["publish_date"]

        data["is_published"] = boolen_checker(data.get("is_published"))
        # data['main_page'] = boolen_checker(data.get('main_page'))

        obj = self.model(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            obj.thumbnail = thumbnail

        obj.save()

        images = request.FILES.getlist("image")
        if images:
            for image in images:
                PhotoGalleryImage.objects.create(photo_gallery=obj, image=image)

        # obj.save()
        return HttpResponseRedirect(self.success_url)


class PhotoList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = PhotoGallery
    form_class = forms.PhotoForm
    queryset = model.objects.all()
    template_name = "back/press_service/photo_gallery_list.html"


class PhotoUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = PhotoGallery
    form_class = forms.PhotoForm
    context_object_name = "object"
    template_name = "back/press_service/photo_gallery_update.html"
    success_url = reverse_lazy("gallery:photo-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])

        data["is_published"] = boolen_checker(data.get("is_published"))
        # obj.main_page = boolen_checker(data.get('main_page'))

        if not data["publish_date"]:
            del data["publish_date"]

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            obj.thumbnail = thumbnail

        images = request.FILES.getlist("image")

        if images:
            for image in images:
                image, _ = PhotoGalleryImage.objects.get_or_create(photo_gallery=obj, image=image)

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.publish_date = data.get("publish_date")
        obj.is_published = data.get("is_published")

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PhotoDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = PhotoGallery
    success_url = reverse_lazy("gallery:photo-list")


class PhotoImageDelete(HasRoleMixin, DeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = PhotoGalleryImage
    success_url = reverse_lazy("gallery:photo-list")

    def get(self, request, pk):
        obj = self.model.objects.get(id=pk)
        # Static page id
        pk = obj.photo_gallery.id
        obj.delete()
        return redirect("gallery:photo-update", pk=int(pk))


# VIDEOGALLAERY VIEWS


class VideoCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = VideoGallery
    form_class = forms.VideoForm
    template_name = "back/press_service/video_gallery_create.html"
    success_url = reverse_lazy("gallery:video-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        data["is_published"] = boolen_checker(data.get("is_published"))
        # data['main_page'] = boolen_checker(data.get('main_page'))

        if not data["publish_date"]:
            del data["publish_date"]

        video_gallery = self.model(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            video_gallery.thumbnail = thumbnail

        video_gallery.save()
        return HttpResponseRedirect(self.success_url)


class VideoList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = VideoGallery
    queryset = model.objects.all()
    template_name = "back/press_service/video_gallery_list.html"


class VideoUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = VideoGallery
    form_class = forms.VideoForm
    context_object_name = "object"
    template_name = "back/press_service/video_gallery_update.html"
    success_url = reverse_lazy("gallery:video-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        if not data["publish_date"]:
            del data["publish_date"]

        thumbnail = request.FILES.get("thumbnail")

        if thumbnail:
            obj.thumbnail = thumbnail

        obj.video_link = data.get("video_link")
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.publish_date = data.get("publish_date")
        obj.is_published = boolen_checker(data.get("is_published"))
        # obj.main_page = boolen_checker(data.get('main_page'))

        obj.save()
        return HttpResponseRedirect(self.success_url)


class VideoDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = VideoGallery
    success_url = reverse_lazy("gallery:video-list")


# Vebinar


class VebinarCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Vebinar
    form_class = forms.VebinarForm
    template_name = "back/press_service/vebinar_create.html"
    success_url = reverse_lazy("gallery:vebinar-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        data["is_published"] = boolen_checker(data.get("is_published"))
        data["main_page"] = boolen_checker(data.get("main_page"))

        if not data["publish_date"]:
            del data["publish_date"]

        vebinar = self.model(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            vebinar.thumbnail = thumbnail

        vebinar.save()
        return HttpResponseRedirect(self.success_url)


class VebinarList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Vebinar
    queryset = model.objects.all()
    template_name = "back/press_service/vebinar_list.html"


class VebinarUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Vebinar
    form_class = forms.VebinarForm
    context_object_name = "object"
    template_name = "back/press_service/vebinar_update.html"
    success_url = reverse_lazy("gallery:vebinar-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        if not data["publish_date"]:
            del data["publish_date"]

        thumbnail = request.FILES.get("thumbnail")

        if thumbnail:
            obj.thumbnail = thumbnail

        obj.video_link = data.get("video_link")
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.author_uz = data.get("author_uz")
        obj.author_ru = data.get("author_ru")
        obj.author_en = data.get("author_en")

        obj.publish_date = data.get("publish_date")
        obj.is_published = boolen_checker(data.get("is_published"))
        obj.main_page = boolen_checker(data.get("main_page"))

        obj.save()
        return HttpResponseRedirect(self.success_url)


class VebinarDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Vebinar
    success_url = reverse_lazy("gallery:vebinar-list")
