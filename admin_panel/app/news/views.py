from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from image_optimizer.utils import image_optimizer

from admin_panel.app import views as custom
from admin_panel.app.news import forms
from admin_panel.model import press_service as news
from admin_panel.model.press_service import Gallery
from admin_panel.model.user import CustomUser


def clean_objective_ids(objective_ids: list) -> list:
    """Return existing Objective IDs from a list of IDs."""

    valid_objective_ids = []

    for objective_id in objective_ids:
        try:
            objective_id = int(objective_id)
            if news.Objective.objects.filter(pk=objective_id).exists():
                valid_objective_ids.append(objective_id)
        except (ValueError, TypeError):
            pass

    return valid_objective_ids


class HasRoleMixin:
    pass


class NewsCreate(CreateView):
    model = news.News
    form_class = forms.NewsForm
    template_name = "back/press_service/news/news_create.html"
    success_url = reverse_lazy("news:news-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = news.NewsCategory.objects.all()
        context["news_hashtags"] = news.NewsHashtag.objects.all()
        context["news_objectives"] = news.Objective.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        hashtags = request.POST.getlist("hashtag")
        objectives = clean_objective_ids(request.POST.getlist("objectives"))

        if data.get("category"):
            data["category"] = news.NewsCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]

        if data.get("objectives"):
            del data["objectives"]

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False

        if not data["publish_date"]:
            del data["publish_date"]

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        obj.objectives.set(objectives)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()

        images = request.FILES.getlist("images")
        if images:
            for image in images:
                Gallery.objects.create(news=obj, image=image)

        return HttpResponseRedirect(self.success_url)


class NewsUpdate(UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.News
    form_class = forms.NewsForm
    context_object_name = "news"
    template_name = "back/press_service/news/news_update.html"
    success_url = reverse_lazy("news:news-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = news.NewsCategory.objects.all()
        context["news_hashtags"] = news.NewsHashtag.objects.all()
        context["news_objectives"] = news.Objective.objects.all()

        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        hashtags = request.POST.getlist("hashtag")
        objectives = clean_objective_ids(request.POST.getlist("objectives"))
        if data.get("category"):
            data["category"] = news.NewsCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]
        if data.get("objectives"):
            del data["objectives"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False

        if not data["publish_date"]:
            del data["publish_date"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.objectives.set(objectives)

        obj.category = data["category"]
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.short_description_uz = data.get("short_description_uz")
        obj.short_description_ru = data.get("short_description_ru")
        obj.short_description_en = data.get("short_description_en")

        obj.publish_date = data.get("publish_date")
        obj.is_published = data.get("is_published")
        obj.main_page = data.get("main_page")

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image

        # obj.video_link = data.get('video_link')

        for i in obj.hashtag.all():
            obj.hashtag.remove(i)

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_en=hashtag)
                if tag not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_ru=hashtag)
                if tag not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = news.NewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = news.NewsHashtag.objects.create(title_uz=hashtag)
                if obj not in obj.hashtag.all():
                    obj.hashtag.add(tag.id)

        obj.save()

        images = request.FILES.getlist("images")
        if images:
            for image in images:
                Gallery.objects.create(news=obj, image=image)

        return HttpResponseRedirect(self.success_url)


class NewsList(custom.CustomListView):
    model = news.News
    template_name = "back/press_service/news/news_list.html"
    queryset = model.objects.all()


class NewsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.News
    success_url = reverse_lazy("news:news-list")


class ObjectiveList(custom.CustomListView):
    model = news.Objective
    template_name = "back/press_service/objective/objective_list.html"
    queryset = model.objects.all()


class ObjectiveCreate(CreateView):
    model = news.Objective
    form_class = forms.ObjectiveForm
    template_name = "back/press_service/objective/objective_create.html"
    success_url = reverse_lazy("news:objective-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ObjectiveCreate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.create(**data)
        icon = request.FILES.get("icon")
        if icon:
            obj.icon = icon
            obj.icon.save(icon.name, icon, save=True)
        return HttpResponseRedirect(self.success_url)


class ObjectiveUpdate(UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.Objective
    form_class = forms.ObjectiveForm
    context_object_name = "objective"
    template_name = "back/press_service/objective/objective_update.html"
    success_url = reverse_lazy("news:objective-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ObjectiveUpdate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.filter(pk=self.kwargs["pk"]).first()
        form = self.form_class(data=request.POST, files=request.FILES, instance=obj)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(self.success_url)


class ObjectiveDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.Objective
    success_url = reverse_lazy("news:objective-list")


#   _____ _             _
#  | ____| | ___  _ __ | | __ _ _ __
#  |  _| | |/ _ \| '_ \| |/ _` | '__|
#  | |___| | (_) | | | | | (_| | |
#  |_____|_|\___/|_| |_|_|\__,_|_|


# class ElonlarCreate(CreateView):
#     model = news.Elonlar
#     form_class = forms.ElonlarForm
#     template_name = 'back/press_service/elonlar/elonlar_create.html'
#     success_url = reverse_lazy('news:elonlar-list')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ElonlarCreate, self).get_context_data(
#             object_list=object_list, **kwargs)
#         # context['news_categories'] = news.NewsCategory.objects.all()
#         # context['news_hashtags'] = news.NewsHashtag.objects.all()
#         if not self.request.user.is_superuser:
#             context['staff'] = CustomUser.objects.get(user=self.request.user)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST.dict()
#         del data['csrfmiddlewaretoken']
#         # hashtags = request.POST.getlist('hashtag')
#
#         # if data.get('category'):
#         #     data['category'] = news.NewsCategory.objects.get(id=int(data['category']))
#
#         # if data.get('hashtag'):
#         #     del data['hashtag']
#         if data.get('is_published') == 'on':
#             data['is_published'] = True
#         else:
#             data['is_published'] = False
#
#         if data.get('main_page') == 'on':
#             data['main_page'] = True
#         else:
#             data['main_page'] = False
#
#         if not data['publish_date']:
#             del data['publish_date']
#
#         # obj = self.model(**data)
#         obj = self.model.objects.create(**data)
#
#         thumbnail = request.FILES.get('thumbnail')
#         if thumbnail:
#             obj.thumbnail = thumbnail
#             obj.cover = thumbnail
#
#         image = request.FILES.get('image')
#         if image:
#             obj.image = image
#
#         # if request.LANGUAGE_CODE == 'en':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_en=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_en=hashtag)
#
#         #         obj.hashtag.add(tag.id)
#
#         # elif request.LANGUAGE_CODE == 'ru':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_ru=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_ru=hashtag)
#
#         #         obj.hashtag.add(tag.id)
#
#         # elif request.LANGUAGE_CODE == 'uz':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_uz=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_uz=hashtag)
#
#         #         obj.hashtag.add(tag.id)
#
#         obj.save()
#         return HttpResponseRedirect(self.success_url)


# class ElonlarUpdate(UpdateView):
#     model = news.Elonlar
#     form_class = forms.ElonlarForm
#     context_object_name = 'news'
#     template_name = 'back/press_service/elonlar/elonlar_update.html'
#     success_url = reverse_lazy('news:elonlar-list')
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ElonlarUpdate, self).get_context_data(
#             object_list=object_list, **kwargs)
#         # context['news_categories'] = news.NewsCategory.objects.all()
#         # context['news_hashtags'] = news.NewsHashtag.objects.all()
#         if not self.request.user.is_superuser:
#             context['staff'] = CustomUser.objects.get(user=self.request.user)
#
#         return context
#
#     def post(self, request, *args, **kwargs):
#         data = request.POST.dict()
#         del data['csrfmiddlewaretoken']
#
#         # hashtags = request.POST.getlist('hashtag')
#         # if data.get('category'):
#         #     data['category'] = news.NewsCategory.objects.get(id=int(data['category']))
#
#         # if data.get('hashtag'):
#         #     del data['hashtag']
#         if data.get('is_published') == 'on':
#             data['is_published'] = True
#         else:
#             data['is_published'] = False
#
#         if data.get('main_page') == 'on':
#             data['main_page'] = True
#         else:
#             data['main_page'] = False
#
#         if not data['publish_date']:
#             del data['publish_date']
#
#         obj = self.model.objects.get(id=self.kwargs['pk'])
#         # obj.category = data['category']
#         obj.title_uz = data.get('title_uz')
#         obj.title_ru = data.get('title_ru')
#         obj.title_en = data.get('title_en')
#
#         obj.description_uz = data.get('description_uz')
#         obj.description_ru = data.get('description_ru')
#         obj.description_en = data.get('description_en')
#
#         # obj.short_description_uz = data.get('short_description_uz')
#         # obj.short_description_ru = data.get('short_description_ru')
#         # obj.short_description_en = data.get('short_description_en')
#
#         obj.publish_date = data.get('publish_date')
#         obj.is_published = data.get('is_published')
#         obj.main_page = data.get('main_page')
#
#         thumbnail = request.FILES.get('thumbnail')
#         if thumbnail:
#             obj.thumbnail = thumbnail
#             obj.cover = thumbnail
#
#         image = request.FILES.get('image')
#         if image:
#             obj.image = image
#
#         # obj.video_link = data.get('video_link')
#
#         # for i in obj.hashtag.all():
#         #     obj.hashtag.remove(i)
#
#         # if request.LANGUAGE_CODE == 'en':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_en=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_en=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_en=hashtag)
#         #         if tag not in obj.hashtag.all():
#         #             obj.hashtag.add(tag.id)
#
#         # elif request.LANGUAGE_CODE == 'ru':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_ru=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_ru=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_ru=hashtag)
#         #         if tag not in obj.hashtag.all():
#         #             obj.hashtag.add(tag.id)
#
#         # elif request.LANGUAGE_CODE == 'uz':
#         #     for hashtag in hashtags:
#         #         if news.NewsHashtag.objects.filter(title_uz=hashtag).exists():
#         #             tag = news.NewsHashtag.objects.get(title_uz=hashtag)
#         #         else:
#         #             tag = news.NewsHashtag.objects.create(title_uz=hashtag)
#         #         if obj not in obj.hashtag.all():
#         #             obj.hashtag.add(tag.id)
#
#         obj.save()
#         return HttpResponseRedirect(self.success_url)


# class ElonlarList(custom.CustomListView):
#     model = news.Elonlar
#     template_name = 'back/press_service/elonlar/elonlar_list.html'
#     queryset = model.objects.all()


# class ElonlarDelete(HasRoleMixin, custom.CustomDeleteView):
#     allowed_roles = 'admin'
#     redirect_to_login = 'login'
#     model = news.Elonlar
#     success_url = reverse_lazy('news:elonlar-list')


class NewsCategoryCreate(custom.CustomCreateView):
    model = news.NewsCategory
    form_class = forms.NewsCategoryForm
    template_name = "back/press_service/news/news_category_create.html"
    success_url = reverse_lazy("news:category-list")


class NewsCategoryUpdate(UpdateView):
    model = news.NewsCategory
    form_class = forms.NewsCategoryForm
    context_object_name = "object"
    template_name = "back/press_service/news/news_category_update.html"
    success_url = reverse_lazy("news:category-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.order = data["order"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsCategoryList(custom.CustomListView):
    model = news.NewsCategory
    template_name = "back/press_service/news/news_category_list.html"
    queryset = model.objects.all()


class NewsCategoryDelete(custom.CustomDeleteView):
    model = news.NewsCategory
    success_url = reverse_lazy("news:category-list")


class NewsHashtagCreate(custom.CustomCreateView):
    model = news.NewsHashtag
    form_class = forms.NewsHashtagForm
    template_name = "back/press_service/news/news_hashtag_create.html"
    success_url = reverse_lazy("news:hashtag-list")


class NewsHashtagUpdate(UpdateView):
    model = news.NewsHashtag
    form_class = forms.NewsHashtagForm
    context_object_name = "object"
    template_name = "back/press_service/news/news_hashtag_update.html"
    success_url = reverse_lazy("news:hashtag-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsHashtagList(custom.CustomListView):
    model = news.NewsHashtag
    template_name = "back/press_service/news/news_hashtag_list.html"
    queryset = model.objects.all()


class NewsHashtagDelete(custom.CustomDeleteView):
    model = news.NewsHashtag
    success_url = reverse_lazy("news:hashtag-list")


# FAQ


class FAQCreate(HasRoleMixin, custom.CustomCreateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.FAQ
    template_name = "back/press_service/faq/create.html"
    form_class = forms.FAQForm
    success_url = reverse_lazy("news:faq-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FAQCreate, self).get_context_data(object_list=object_list, **kwargs)

        return context


class FAQUpdate(HasRoleMixin, UpdateView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.FAQ
    template_name = "back/press_service/faq/update.html"
    form_class = forms.FAQForm
    context_object_name = "object"
    success_url = reverse_lazy("news:faq-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(FAQUpdate, self).get_context_data(object_list=object_list, **kwargs)

        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.author_uz = data["author_uz"]
        obj.author_ru = data["author_ru"]
        obj.author_en = data["author_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class FAQDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.FAQ
    success_url = reverse_lazy("news:faq-list")


class FAQList(HasRoleMixin, custom.CustomListView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = news.FAQ
    template_name = "back/press_service/faq/list.html"
    queryset = model.objects.all()


class PhotoGallaeryImageDeleteView(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = Gallery

    def get(self, *args, **kwargs):
        pk = self.kwargs["pk"]
        pk = Gallery.objects.get(pk=int(pk)).news_id
        super().get(*args, **kwargs)
        return redirect(reverse_lazy("news:news-update", args=(pk,)))
