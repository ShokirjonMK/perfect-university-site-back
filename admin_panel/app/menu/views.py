from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.views import APIView
from rolepermissions.mixins import HasRoleMixin

from django.utils.translation import gettext as _
from sentry_sdk import capture_exception

from admin_panel.model.menu import Menu
from django.views.generic import CreateView

from config import settings
from . import forms, serializers
from django.db import transaction


# API create & update
# class MenuCreateAPIView(generics.CreateAPIView):
class MenuCreateAPIView(HasRoleMixin, APIView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    queryset = Menu.objects.all()
    serializer_class = serializers.MenuSerializer
    success_url = reverse_lazy("menu:menu-list")

    def get(self, request):
        parent = Menu.objects.filter(parent__isnull=True)
        serializer = serializers.MenuListSerializer(parent, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return Response("success", status=201)


class MenuCreateAPI(HasRoleMixin, APIView):
    allowed_roles = "admin"
    redirect_to_login = "login"

    def post(self, request, *args, **kwargs):
        data = request.data.get("payload")

        try:
            with transaction.atomic():
                Menu.objects.all().delete()
                for parent in data:
                    new_parent = Menu.objects.create(
                        title_uz=parent["title_uz"],
                        title_ru=parent["title_ru"],
                        title_en=parent["title_en"],
                        description_uz=parent["description_uz"],
                        description_ru=parent["description_ru"],
                        description_en=parent["description_en"],
                        order=parent["order"],
                        footer=parent["footer"],
                        only_footer=parent["only_footer"],
                        url=parent["url"],
                    )
                    if parent.get("child"):
                        # print('creating child')
                        for child in parent["child"]:
                            Menu.objects.create(
                                title_uz=child["title_uz"],
                                title_ru=child["title_ru"],
                                title_en=child["title_en"],
                                description_uz=child["description_uz"],
                                description_ru=child["description_ru"],
                                description_en=child["description_en"],
                                order=child["order"],
                                footer=child["footer"],
                                only_footer=child["only_footer"],
                                is_static=child["is_static"],
                                parent=new_parent,
                                url=child["url"],
                            )

                return Response(_("Muvaffaqiyatli saqlandi"), status=201)
        except Exception as e:
            capture_exception(e)
            return Response(_("Xatolik yuz berdi"), status=200)


class MenuDeleteAPI(HasRoleMixin, APIView):
    allowed_roles = "admin"
    redirect_to_login = "login"

    def post(self, request, *args, **kwargs):
        data = self.request.data.get("id")
        obj = Menu.objects.filter(id=int(data))
        if obj.exists():
            obj.last().delete()
            return Response("Menu deleted")
        else:
            return Response("Menu not deleted")


class MenuCreate(HasRoleMixin, CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Menu
    form_class = forms.MenuForm
    template_name = "back/menu/menu_create.html"
    success_url = reverse_lazy("menu:menu-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MenuCreate, self).get_context_data(object_list=object_list)
        api_url = "menu/api/"
        host = self.request.build_absolute_uri("/")[:-1]
        api = "%s/%s%s" % (host, "", api_url)
        post = "%s/%s%screate/" % (host, "", api_url)
        delete = "%s/%s%sdelete/" % (host, "", api_url)
        context["api"] = api
        context["post"] = post
        context["delete"] = delete
        context["host"] = settings.FRONT
        return context

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.success_url)
