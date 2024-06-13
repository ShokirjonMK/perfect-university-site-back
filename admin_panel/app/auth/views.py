from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.utils.translation import gettext_lazy as _

from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from admin_panel.admin import LoginForm


class Login(LoginView):
    form_class = LoginForm
    template_name = "back/auth/login.html"

    def get_success_url(self):
        return reverse_lazy("index-admin")


# class Login(View):
#     def get(self, request):
#         return render(request, 'back/auth/login.html', {})
#
#     def post(self, request):
#
#         recaptcha_response = request.POST.get('g-recaptcha-response')
#         data = {
#             'secret': settings.RECAPTCHA_PRIVATE_KEY,
#             'response': recaptcha_response
#         }
#         r = requests.post(
#             'https://www.google.com/recaptcha/api/siteverify', data=data)
#         result = r.json()
#         ''' End reCAPTCHA validation '''
#         if result['success']:
#             data = request.POST.dict()
#             username = data.get('username')
#             password = data.get('password')
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('index-admin'))
#             return render(request, 'back/auth/login.html', {'error_nouser': True})
#         messages.error(request, 'Не удалось провести проверку CAPTCHA.')
#         return render(request, 'back/auth/login.html', {})


class Profile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "back/auth/profile.html")

    def post(self, request):
        data = request.POST.dict()
        username = data.get("username")
        old_password = data.get("old_password")
        new_password = data.get("new_password")
        confirm_pass = data.get("confirm_pass")

        user = User.objects.get(id=self.request.user.id)
        if user.check_password(old_password):
            if new_password == confirm_pass:
                user.username = username
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, _("Parolingiz muvaffaqiyatli yangilandi."))
                return HttpResponseRedirect(reverse("profile"))
            else:
                return render(request, "back/auth/profile.html", {"error_confirm": True})
        else:
            return render(request, "back/auth/profile.html", {"error_old": True})


class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))
