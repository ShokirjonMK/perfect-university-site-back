from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from config.swagger_schema import schema_view

from django.contrib.auth.forms import AuthenticationForm
from captcha import fields


# class LoginForm(AuthenticationForm):
#     captcha = fields.ReCaptchaField()

#     def clean(self):
#         captcha = self.cleaned_data.get("captcha")
#         if not captcha:
#             return
#         return super().clean()


# admin.site.login_form = LoginForm
admin.site.login_template = "login.html"


# from admin_panel.typo.views import TypoView
from PIL.JpegImagePlugin import RAWMODE

RAWMODE.update(
    {
        "RGBA": "RGB",  # RGBA error fix
    }
)
# from front.error.views import handler404 as page404
# handler404 = 'front.error.views.handler404'
# handler500 = 'front.error.views.handler500'
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("api/v1/syllabus/", include("syllabus.urls")),
    path("syllabus/", include("syllabus.d_urls")),
    path("hr/api/v1/", include("hr.panel_api.urls")),
    path("hr/transfer/", include("hr.transfer_api.urls")),
    path("api/v1/vacancy-form/", include("hr.api.urls")),
    path("hr/", include("hr.urls")),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    re_path("rosetta/", include("rosetta.urls")),
    # path("", include("admin_panel.urls")),
    # path('error/', TypoView.as_view(), name='typo_reporting_form_url'),
]

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))

# urlpatterns += i18n_patterns(
#     path('api/panel/', include('admin_panel.urls')),
#     # path('', include('front.urls')),
# )

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
