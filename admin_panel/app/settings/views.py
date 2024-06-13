from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.mixins import HasRoleMixin
from admin_panel.app import views as custom
from api import serializers
from . import forms
from admin_panel.model.settings import MainPageSetting, Slider, TopLink, Sidebar
from django.utils.translation import gettext as _


# class GeneralSettings(HasRoleMixin, View):
#     allowed_roles = 'admin'
#     redirect_to_login = 'login'
#     model = MainPageSetting
#     success_url = reverse_lazy('settings:general')
#
#     def get(self, request):
#         if self.model.objects.last():
#             site = self.model.objects.last()
#         else:
#             site = self.model.objects.create()
#         return render(request, 'back/settings/main_page_settings.html', {'site': site})
#
#     def post(self, request):
#         data = request.POST.dict()
#         del data['csrfmiddlewaretoken']
#
#
#         site = self.model.objects.last()
#         for key, value in data.items():
#             if hasattr(site,key) and value:
#                 setattr(site,key,value)
#         site.save()
#
#         #Hard code
#         #banner
#         banner_uz = request.FILES.get('banner_uz', False)
#         banner_ru = request.FILES.get('banner_ru', False)
#         banner_en = request.FILES.get('banner_en', False)
#         banner_sr = request.FILES.get('banner_sr', False)
#
#         if banner_uz:
#             site.banner_uz = banner_uz
#         if banner_ru:
#             site.banner_ru = banner_ru
#         if banner_en:
#             site.banner_en = banner_en
#         if banner_sr:
#             site.banner_sr = banner_sr
#
#         #logo
#         logo_uz = request.FILES.get('logo_uz', False)
#         logo_ru = request.FILES.get('logo_ru', False)
#         logo_en = request.FILES.get('logo_en', False)
#         logo_sr = request.FILES.get('logo_sr', False)
#
#         if logo_uz:
#             site.logo_uz = logo_uz
#         if logo_ru:
#             site.logo_ru = logo_ru
#         if logo_en:
#             site.logo_en = logo_en
#         if logo_sr:
#             site.logo_sr = logo_sr
#
#
#         #logo
#         logo_white_uz = request.FILES.get('logo_white_uz', False)
#         logo_white_ru = request.FILES.get('logo_white_ru', False)
#         logo_white_en = request.FILES.get('logo_white_en', False)
#         logo_white_sr = request.FILES.get('logo_white_sr', False)
#
#
#         if logo_white_uz:
#             site.logo_white_uz = logo_white_uz
#         if logo_white_ru:
#             site.logo_white_ru = logo_white_ru
#         if logo_white_en:
#             site.logo_white_en = logo_white_en
#         if logo_white_sr:
#             site.logo_white_sr = logo_white_sr
#
#         site.save()
#         return HttpResponseRedirect(self.success_url)


class MainSettingsView(HasRoleMixin, View):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = MainPageSetting
    success_url = reverse_lazy("settings:general")

    def get(self, request):
        if self.model.objects.last():
            site = self.model.objects.last()
        else:
            site = self.model.objects.create()
        return render(request, "back/settings/main_page.html", {"site": site})

    def post(self, request):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        site = self.model.objects.last()
        for key, value in data.items():
            if hasattr(site, key) and value:
                setattr(site, key, value)
        site.save()

        # Hard code
        # banner
        # banner_uz = request.FILES.get('banner_uz', False)
        # banner_ru = request.FILES.get('banner_ru', False)
        # banner_en = request.FILES.get('banner_en', False)
        # banner_sr = request.FILES.get('banner_sr', False)
        #
        # if banner_uz:
        #     site.banner_uz = banner_uz
        # if banner_ru:
        #     site.banner_ru = banner_ru
        # if banner_en:
        #     site.banner_en = banner_en
        # if banner_sr:
        #     site.banner_sr = banner_sr

        # logo
        logo_uz = request.FILES.get("logo_uz", False)
        logo_ru = request.FILES.get("logo_ru", False)
        logo_en = request.FILES.get("logo_en", False)
        # logo_sr = request.FILES.get('logo_sr', False)

        if logo_uz:
            site.logo_uz = logo_uz
        if logo_ru:
            site.logo_ru = logo_ru
        if logo_en:
            site.logo_en = logo_en
        # if logo_sr:
        #     site.logo_sr = logo_sr

        # logo
        logo_white_uz = request.FILES.get("logo_white_uz", False)
        logo_white_ru = request.FILES.get("logo_white_ru", False)
        logo_white_en = request.FILES.get("logo_white_en", False)
        # logo_white_sr = request.FILES.get('logo_white_sr', False)

        if logo_white_uz:
            site.logo_white_uz = logo_white_uz
        if logo_white_ru:
            site.logo_white_ru = logo_white_ru
        if logo_white_en:
            site.logo_white_en = logo_white_en
        # if logo_white_sr:
        #     site.logo_white_sr = logo_white_sr

        site.save()
        return HttpResponseRedirect(self.success_url)


class SliderList(HasRoleMixin, custom.CustomListView):
    template_name = "back/settings/slider/list.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Slider
    queryset = model.objects.all()


class SliderCreate(HasRoleMixin, custom.CustomCreateView):
    template_name = "back/settings/slider/create.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Slider
    form_class = forms.SliderForm
    queryset = model.objects.all()
    success_url = reverse_lazy("settings:slider-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)

        image_uz = request.FILES.get("image_uz")
        image_ru = request.FILES.get("image_ru")
        image_en = request.FILES.get("image_en")
        if image_uz:
            obj.image_uz = image_uz
        if image_ru:
            obj.image_ru = image_ru
        if image_en:
            obj.image_en = image_en
        obj.save()
        return HttpResponseRedirect(self.success_url)


class SliderUpdate(HasRoleMixin, custom.CustomUpdateView):
    template_name = "back/settings/slider/update.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Slider
    form_class = forms.SliderForm
    queryset = model.objects.all()
    success_url = reverse_lazy("settings:slider-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(pk=self.kwargs.get("pk"))

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.short_description_uz = data.get("short_description_uz")
        obj.short_description_ru = data.get("short_description_ru")
        obj.short_description_en = data.get("short_description_en")
        obj.order = data.get("order")
        obj.link = data.get("link")

        image_uz = request.FILES.get("image_uz")
        image_ru = request.FILES.get("image_ru")
        image_en = request.FILES.get("image_en")
        if image_uz:
            obj.image_uz = image_uz
        if image_ru:
            obj.image_ru = image_ru
        if image_en:
            obj.image_en = image_en

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SliderDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Slider
    success_url = reverse_lazy("settings:slider-list")


# TopLink
class TopLinkList(HasRoleMixin, custom.CustomListView):
    template_name = "back/settings/top-link/list.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = TopLink
    queryset = model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top_links"] = TopLink.objects.all()
        context["post"] = reverse("settings:top-link-create")
        context["api"] = reverse("settings:top-link-api")
        return context


class TopLinkListApi(HasRoleMixin, APIView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    queryset = TopLink.objects.all()
    serializer_class = serializers.MenuSerializer
    success_url = reverse_lazy("menu:menu-list")

    def get(self, request, format=None):
        parent = TopLink.objects.filter(parent__isnull=True)
        serializer = serializers.TopLinkSerializer(parent, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return Response("success", status=201)


class TopLinkCreate(HasRoleMixin, APIView):
    allowed_roles = "admin"
    redirect_to_login = "login"

    def post(self, request, *args, **kwargs):
        data = request.data.get("payload")

        # try:
        with transaction.atomic():
            TopLink.objects.all().delete()
            for parent in data:
                print(parent)
                new_parent = TopLink.objects.create(
                    title_uz=parent["title_uz"],
                    title_ru=parent["title_ru"],
                    title_en=parent["title_en"],
                    order=parent["order"],
                    link=parent["link"],
                )
                if parent.get("child") if "child" in parent else None:
                    # print('creating child')
                    for child in parent["child"] if "child" in parent else []:
                        print(child)
                        TopLink.objects.create(
                            title_uz=child["title_uz"],
                            title_ru=child["title_ru"],
                            title_en=child["title_en"],
                            order=child["order"],
                            parent=new_parent,
                            link=child["link"],
                        )

            return Response(_("Muvaffaqiyatli saqlandi"), status=201)

    # except Exception as e:
    #     print(e)
    #     return Response(_("Xatolik yuz berdi"), status=200)


class TopLinkUpdate(HasRoleMixin, custom.CustomUpdateView):
    template_name = "back/settings/top-link/update.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = TopLink
    form_class = forms.TopLinkForm
    queryset = model.objects.all()
    success_url = reverse_lazy("settings:top-link-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(pk=self.kwargs.get("pk"))

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.order = data.get("order")
        obj.link = data.get("link")

        obj.save()
        return HttpResponseRedirect(self.success_url)


class TopLinkDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = TopLink
    success_url = reverse_lazy("settings:top-link-list")


# Sidebar
class SidebarList(HasRoleMixin, custom.CustomListView):
    template_name = "back/settings/sidebar/list.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Sidebar
    queryset = model.objects.all()


class SidebarCreate(HasRoleMixin, custom.CustomCreateView):
    template_name = "back/settings/sidebar/create.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Sidebar
    form_class = forms.SidebarForm
    queryset = model.objects.all()
    success_url = reverse_lazy("settings:sidebar-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.create(**data)
        image = request.FILES.get("image")
        if image:
            obj.image = image
        obj.save()
        return HttpResponseRedirect(self.success_url)


class SidebarUpdate(HasRoleMixin, custom.CustomUpdateView):
    template_name = "back/settings/sidebar/update.html"
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Sidebar
    form_class = forms.SidebarForm
    queryset = model.objects.all()
    success_url = reverse_lazy("settings:sidebar-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(pk=self.kwargs.get("pk"))

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")
        obj.button_title_uz = data.get("button_title_uz")
        obj.button_title_ru = data.get("button_title_ru")
        obj.button_title_en = data.get("button_title_en")

        obj.order = data.get("order")
        obj.link = data.get("link")
        image = request.FILES.get("image")
        if image:
            obj.image = image

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SidebarDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Sidebar
    success_url = reverse_lazy("settings:sidebar-list")
