from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from rolepermissions.mixins import HasRoleMixin

from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import CreateCustomUserForm
from django.contrib import messages
from django.views import generic
from admin_panel.app import views as custom
from admin_panel.model.user import CustomUser
from django.utils.translation import gettext_lazy as _
from rolepermissions.roles import assign_role, clear_roles


class CreateCustomUserView(HasRoleMixin, generic.CreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = CustomUser
    template_name = "back/user/user_create.html"
    form_class = CreateCustomUserForm
    success_url = reverse_lazy("user:user-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        username = data["username"]
        password = data["password"]

        if User.objects.filter(username=username).exists():
            messages.success(request, _("Bunday foydalanuvchi avval ro'yxatdan o'tgan"))
            return HttpResponseRedirect(reverse_lazy("user:user-create"))

        user = User.objects.create(
            username=username, password=password, is_active=True, is_staff=True, is_superuser=False
        )
        if data.get("main_page") == "on":
            assign_role(user, "admin")
        else:
            assign_role(user, "staff")
        user.set_password(password)
        user.save()

        obj = self.model.objects.create(user=user, email=data["email"], phone=data["phone"])

        obj.save()
        return HttpResponseRedirect(self.success_url)


class UpdateCustomUserView(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    template_name = "back/user/user_update.html"
    form_class = CreateCustomUserForm
    model = CustomUser
    context_object_name = "object"
    success_url = reverse_lazy("user:user-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        username = data["username"]
        password = data["password"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        if obj.user.username != username:
            if User.objects.filter(username=username).exists():
                messages.success(request, _("Bunday foydalanuvchi avval ro'yxatdan o'tgan"))
                return HttpResponseRedirect(reverse_lazy("user:user-update", kwargs={"pk": obj.id}))
            else:
                obj.user.username = username
        if password:
            obj.user.set_password(password)
        clear_roles(obj.user)
        if data.get("main_page") == "on":
            assign_role(obj.user, "admin")
        else:
            assign_role(obj.user, "staff")
        obj.user.save()

        obj.email = data["email"]
        obj.phone = data["phone"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


# class CustomUserList(views.SuperuserRequiredMixin, custom.CustomListView):
class CustomUserList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = CustomUser
    queryset = model.objects.filter(user__is_superuser=False)
    template_name = "back/user/user_list.html"
    permission_required = "auth.user.manage"


class CustomUserDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = CustomUser
    success_url = reverse_lazy("user:user-list")
