from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from admin_panel.model import press_service as news
from admin_panel.app.science import forms
from admin_panel.model import science as science
from admin_panel.app import views as custom
from admin_panel.model.user import CustomUser
from admin_panel.common import boolen_checker
from image_optimizer.utils import image_optimizer


class HasRoleMixin:
    pass


class NewsCreate(CreateView):
    model = science.ScienceNews
    form_class = forms.NewsForm
    template_name = "back/science/news/news_create.html"
    success_url = reverse_lazy("science:news-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = science.ScienceNewsCategory.objects.all()
        context["news_hashtags"] = science.ScienceNewsHashtag.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        hashtags = request.POST.getlist("hashtag")

        if data.get("category"):
            data["category"] = science.ScienceNewsCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if not data["publish_date"]:
            del data["publish_date"]
        obj = self.model.objects.create(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsUpdate(UpdateView):
    model = science.ScienceNews
    form_class = forms.NewsForm
    context_object_name = "news"
    template_name = "back/science/news/news_update.html"
    success_url = reverse_lazy("science:news-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(NewsUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = science.ScienceNewsCategory.objects.all()
        context["news_hashtags"] = science.ScienceNewsHashtag.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        hashtags = request.POST.getlist("hashtag")
        if data.get("category"):
            data["category"] = science.ScienceNewsCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]
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
        obj.category = data["category"]
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.publish_date = data.get("publish_date")
        obj.is_published = data.get("is_published")
        obj.main_page = data.get("main_page")

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image
        for i in obj.hashtag.all():
            obj.hashtag.remove(i)

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_en=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_en=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if science.ScienceNewsHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = science.ScienceNewsHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = science.ScienceNewsHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsList(custom.CustomListView):
    model = science.ScienceNews
    template_name = "back/science/news/news_list.html"
    queryset = model.objects.all()


class NewsDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = science.ScienceNews
    success_url = reverse_lazy("science:news-list")


class ScienceCenterView(custom.CustomListView):
    model = science.ScienceCenter
    template_name = "back/science/science_center/science_center_list.html"
    queryset = model.objects.all()


class ScienceCenterDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = science.ScienceCenter
    success_url = reverse_lazy("science:science-center-list")


class ScienceCenterUpdate(UpdateView):
    model = science.ScienceCenter
    form_class = forms.ScienceCenterForm
    # context_object_name = 'news'
    template_name = "back/science/science_center/science_center_update.html"
    success_url = reverse_lazy("science:science-center-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ScienceCenterUpdate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        # if data.get('category'):
        #     data['category'] = science.ScienceCenter.objects.get(
        #         id=int(data['category']))

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        if data.get("main_page") == "on":
            data["main_page"] = True
        else:
            data["main_page"] = False

        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.reception_time_uz = data.get("reception_time_uz")
        obj.reception_time_ru = data.get("reception_time_ru")
        obj.reception_time_en = data.get("reception_time_en")
        obj.email = data.get("email")
        obj.phone_number = data.get("phone_number")
        obj.fax = data.get("fax")
        obj.is_published = data.get("is_published")
        obj.main_page = data.get("main_page")

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ScienceCenterCreate(CreateView):
    model = science.ScienceCenter
    form_class = forms.ScienceCenterForm
    template_name = "back/science/science_center/science_center_create.html"
    success_url = reverse_lazy("science:science-center-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ScienceCenterCreate, self).get_context_data(object_list=object_list, **kwargs)
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        obj = self.model.objects.create(**data)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsCategoryCreate(custom.CustomCreateView):
    model = science.ScienceNewsCategory
    form_class = forms.NewsCategoryForm
    template_name = "back/science/news/news_category_create.html"
    success_url = reverse_lazy("science:category-list")


class NewsCategoryUpdate(UpdateView):
    model = science.ScienceNewsCategory
    form_class = forms.NewsCategoryForm
    context_object_name = "object"
    template_name = "back/science/news/news_category_update.html"
    success_url = reverse_lazy("science:category-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        # obj.order = data['order']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsCategoryList(custom.CustomListView):
    model = science.ScienceNewsCategory
    template_name = "back/science/news/news_category_list.html"
    queryset = model.objects.all()


class NewsCategoryDelete(custom.CustomDeleteView):
    model = science.ScienceNewsCategory
    success_url = reverse_lazy("science:category-list")


class NewsHashtagCreate(custom.CustomCreateView):
    model = science.ScienceNewsHashtag
    form_class = forms.NewsHashtagForm
    template_name = "back/science/news/news_hashtag_create.html"
    success_url = reverse_lazy("science:hashtag-list")


class NewsHashtagUpdate(UpdateView):
    model = science.ScienceNewsHashtag
    form_class = forms.NewsHashtagForm
    context_object_name = "object"
    template_name = "back/science/news/news_hashtag_update.html"
    success_url = reverse_lazy("science:hashtag-list")

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
    model = science.ScienceNewsHashtag
    template_name = "back/science/news/news_hashtag_list.html"
    queryset = model.objects.all()


class NewsHashtagDelete(custom.CustomDeleteView):
    model = science.ScienceNewsHashtag
    success_url = reverse_lazy("science:hashtag-list")


# files
class NewsFileList(custom.CustomListView):
    model = science.ScienceFiles
    template_name = "back/science/news/news_files_list.html"
    queryset = model.objects.all()


class NewsFileCreate(CreateView):
    model = science.ScienceFiles
    form_class = forms.NewsFileForm
    template_name = "back/science/news/news_files_create.html"
    success_url = reverse_lazy("science:news-file-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        docs = self.model.objects.create(**data)
        file = request.FILES.get("file")
        if file:
            docs.file = file

        docs.save()
        return HttpResponseRedirect(self.success_url)


class NewsFileUpdate(UpdateView):
    model = science.ScienceFiles
    form_class = forms.NewsFileForm
    context_object_name = "object"
    template_name = "back/science/news/news_files_update.html"
    success_url = reverse_lazy("science:news-file-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        # obj.order = data['order']

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class NewsFileDelete(custom.CustomDeleteView):
    model = science.ScienceFiles
    success_url = reverse_lazy("science:news-file-list")


# Seminar


class SeminarCreate(CreateView):
    model = science.Seminar
    form_class = forms.SeminarForm
    template_name = "back/science/seminar/news_create.html"
    success_url = reverse_lazy("science:seminar-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SeminarCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = science.SeminarCategory.objects.all()
        context["news_hashtags"] = science.SeminarCategory.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        hashtags = request.POST.getlist("hashtag")

        if data.get("category"):
            data["category"] = science.SeminarCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        # if data.get('main_page') == 'on':
        #     data['main_page'] = True
        # else:
        #     data['main_page'] = False

        if not data["publish_date"]:
            del data["publish_date"]

        # obj = self.model(**data)
        obj = self.model.objects.create(**data)

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_en=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_en=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SeminarUpdate(UpdateView):
    model = science.Seminar
    form_class = forms.SeminarForm
    context_object_name = "news"
    template_name = "back/science/seminar/news_update.html"
    success_url = reverse_lazy("science:seminar-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SeminarUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["news_categories"] = science.SeminarCategory.objects.all()
        context["news_hashtags"] = science.SeminarHashtag.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        hashtags = request.POST.getlist("hashtag")
        if data.get("category"):
            data["category"] = science.SeminarCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]
        if data.get("is_published") == "on":
            data["is_published"] = True
        else:
            data["is_published"] = False

        # if data.get('main_page') == 'on':
        #     data['main_page'] = True
        # else:
        #     data['main_page'] = False

        if not data["publish_date"]:
            del data["publish_date"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.category = data["category"]
        obj.title_uz = data.get("title_uz")
        obj.title_ru = data.get("title_ru")
        obj.title_en = data.get("title_en")

        obj.description_uz = data.get("description_uz")
        obj.description_ru = data.get("description_ru")
        obj.description_en = data.get("description_en")

        obj.publish_date = data.get("publish_date")
        obj.is_published = data.get("is_published")
        obj.main_page = data.get("main_page")

        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            thumbnail = image_optimizer(image_data=thumbnail, output_size=news.NEWS_THUMBNAIL, resize_method="cover")
            obj.thumbnail = thumbnail
            obj.cover = thumbnail

        image = request.FILES.get("image")
        if image:
            obj.image = image

        for i in obj.hashtag.all():
            obj.hashtag.remove(i)

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_en=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_en=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_ru=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_ru=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if science.SeminarHashtag.objects.filter(title_uz=hashtag).exists():
                    tag = science.SeminarHashtag.objects.get(title_uz=hashtag)
                else:
                    tag = science.SeminarHashtag.objects.create(title_uz=hashtag)

                obj.hashtag.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SeminarList(custom.CustomListView):
    model = science.Seminar
    template_name = "back/science/seminar/news_list.html"
    queryset = model.objects.all()


class SeminarDelete(HasRoleMixin, custom.CustomDeleteView):
    allowed_roles = "admin"
    redirect_to_login = "login"
    model = science.Seminar
    success_url = reverse_lazy("science:seminar-list")


class SeminarCategoryCreate(custom.CustomCreateView):
    model = science.SeminarCategory
    form_class = forms.SeminarCategoryForm
    template_name = "back/science/seminar/news_category_create.html"
    success_url = reverse_lazy("science:seminar-category-list")


class SeminarCategoryUpdate(UpdateView):
    model = science.SeminarCategory
    form_class = forms.SeminarCategoryForm
    context_object_name = "object"
    template_name = "back/science/seminar/news_category_update.html"
    success_url = reverse_lazy("science:seminar-category-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]

        obj = self.model.objects.get(id=self.kwargs["pk"])
        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        # obj.order = data['order']

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SeminarCategoryList(custom.CustomListView):
    model = science.SeminarCategory
    template_name = "back/science/seminar/news_category_list.html"
    queryset = model.objects.all()


class SeminarCategoryDelete(custom.CustomDeleteView):
    model = science.SeminarCategory
    success_url = reverse_lazy("news:seminar-category-list")


class SeminarHashtagCreate(custom.CustomCreateView):
    model = science.SeminarHashtag
    form_class = forms.SeminarHashtagForm
    template_name = "back/science/seminar/news_hashtag_create.html"
    success_url = reverse_lazy("science:seminar-hashtag-list")


class SeminarHashtagUpdate(UpdateView):
    model = science.SeminarHashtag
    form_class = forms.SeminarHashtagForm
    context_object_name = "object"
    template_name = "back/science/seminar/news_hashtag_update.html"
    success_url = reverse_lazy("science:seminar-hashtag-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class SeminarHashtagList(custom.CustomListView):
    model = science.SeminarHashtag
    template_name = "back/science/seminar/news_hashtag_list.html"
    queryset = model.objects.all()


class SeminarHashtagDelete(custom.CustomDeleteView):
    model = science.SeminarHashtag
    success_url = reverse_lazy("science:seminar-hashtag-list")


class MonoArticleList(custom.CustomListView):
    model = science.MonoArticle
    template_name = "back/science/articles/article_list.html"
    queryset = model.objects.all()


class MonoArticleCreate(custom.CustomCreateView):
    model = science.MonoArticle
    template_name = "back/science/articles/article_create.html"
    form_class = forms.MonoArticleForm
    success_url = reverse_lazy("science:article-list")


class MonoArticleDelete(custom.CustomDeleteView):
    model = science.MonoArticle
    success_url = reverse_lazy("science:article-list")


class MonoArticleUpdate(UpdateView):
    model = science.MonoArticle
    form_class = forms.MonoArticleForm
    context_object_name = "object"
    template_name = "back/science/articles/article_update.html"
    success_url = reverse_lazy("science:article-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        if data.get("is_published"):
            obj.is_published = boolen_checker((data.get("is_published")))
        else:
            obj.is_published = False

        obj.save()
        return HttpResponseRedirect(self.success_url)


class MonoSectionList(custom.CustomListView):
    model = science.MonoFiles
    template_name = "back/science/articles/mono_files_list.html"
    queryset = model.objects.all()


class MonoSectionCreate(CreateView):
    model = science.MonoFiles
    template_name = "back/science/articles/mono_files_create.html"
    form_class = forms.MonoFilesForm
    success_url = reverse_lazy("science:mono-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MonoSectionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["articles"] = science.MonoArticle.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("article"):
            data["article"] = science.MonoArticle.objects.get(id=int(data["article"]))

        obj = self.model.objects.create(**data)

        # obj.title_uz = data['title_uz']
        # obj.title_ru = data['title_ru']
        # obj.title_en = data['title_en']
        # obj.article = data['article']
        # obj.order = data['order']
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class MonoSectionUpdate(UpdateView):
    model = science.MonoFiles
    form_class = forms.MonoFilesForm
    context_object_name = "object"
    template_name = "back/science/articles/mono_files_update.html"
    success_url = reverse_lazy("science:mono-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MonoSectionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["articles"] = science.MonoArticle.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        if data.get("article"):
            data["article"] = science.MonoArticle.objects.get(id=int(data["article"]))

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.article = data["article"]
        obj.order = data["order"]
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class MonoSectionDelete(custom.CustomDeleteView):
    model = science.MonoFiles
    success_url = reverse_lazy("science:mono-list")


# Seksiya
class MonoArticleSectionList(custom.CustomListView):
    model = science.Section
    template_name = "back/science/articles/section_list.html"
    queryset = model.objects.all()


class MonoArticleSectionCreate(CreateView):
    model = science.Section
    template_name = "back/science/articles/section_create.html"
    form_class = forms.MonoSectionForm
    success_url = reverse_lazy("science:section-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MonoArticleSectionCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["articles"] = science.MonoArticle.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("article"):
            data["article"] = science.MonoArticle.objects.get(id=int(data["article"]))

        obj = self.model.objects.create(**data)

        # obj.title_uz = data['title_uz']
        # obj.title_ru = data['title_ru']
        # obj.title_en = data['title_en']
        # obj.article = data['article']
        # obj.order = data['order']
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class MonoArticleSectionUpdate(UpdateView):
    model = science.Section
    form_class = forms.MonoSectionForm
    context_object_name = "object"
    template_name = "back/science/articles/section_update.html"
    success_url = reverse_lazy("science:section-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MonoArticleSectionUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["articles"] = science.MonoArticle.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        if data.get("article"):
            data["article"] = science.MonoArticle.objects.get(id=int(data["article"]))

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.article = data["article"]
        obj.order = data["order"]
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class MonoArticleSectionDelete(custom.CustomDeleteView):
    model = science.Section
    success_url = reverse_lazy("science:section-list")


class PendingConferenceList(custom.CustomListView):
    model = science.PendingConference
    template_name = "back/science/pending_conference/pending_conference_list.html"
    queryset = model.objects.all()


class PendingConferenceCreate(CreateView):
    model = science.PendingConference
    template_name = "back/science/pending_conference/pending_conference_create.html"
    form_class = forms.PendingConferenceForm
    success_url = reverse_lazy("science:pending-conference-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PendingConferenceCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["tags"] = science.ConferenceTags.objects.all()
        context["status"] = [
            ("pending", "Kutilmoqda"),
            ("finished", "Tugallangan"),
        ]
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        hashtags = request.POST.getlist("hashtag")

        if data.get("category"):
            data["category"] = science.ScienceNewsCategory.objects.get(id=int(data["category"]))

        if data.get("hashtag"):
            del data["hashtag"]

        obj = self.model.objects.create(**data)

        icon = request.FILES.get("icon")
        if icon:
            obj.icon = icon

        image = request.FILES.get("image")
        if image:
            obj.image = image

        if request.LANGUAGE_CODE == "en":
            for hashtag in hashtags:
                if science.ConferenceTags.objects.filter(name_en=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_en=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_en=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in hashtags:
                if science.ConferenceTags.objects.filter(name_ru=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_ru=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_ru=hashtag)

                obj.hashtag.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in hashtags:
                if science.ConferenceTags.objects.filter(name_uz=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_uz=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_uz=hashtag)

                obj.tags.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PendingConferenceUpdate(UpdateView):
    model = science.PendingConference
    form_class = forms.PendingConferenceForm
    context_object_name = "object"
    template_name = "back/science/pending_conference/pending_conference_update.html"
    success_url = reverse_lazy("science:pending-conference-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PendingConferenceUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["tags"] = science.ConferenceTags.objects.all()
        context["status"] = [
            ("pending", "Kutilmoqda"),
            ("finished", "Tugallangan"),
        ]
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        print(data)
        tags = request.POST.getlist("hashtag")
        if data.get("hashtag"):
            del data["hashtag"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.status = data["status"]

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.description_uz = data["description_uz"]
        obj.description_ru = data["description_ru"]
        obj.description_en = data["description_en"]
        obj.date = data["date"]
        obj.start_time = data["start_time"]
        obj.end_time = data["end_time"]
        image = request.FILES.get("image")
        if image:
            obj.image = image
        icon = request.FILES.get("icon")
        if icon:
            obj.icon = icon

        for i in obj.tags.all():
            obj.tags.remove(i)

        if request.LANGUAGE_CODE == "en":
            for hashtag in tags:
                if science.ConferenceTags.objects.filter(name_en=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_en=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_en=hashtag)

                obj.tags.add(tag.id)

        elif request.LANGUAGE_CODE == "ru":
            for hashtag in tags:
                if science.ConferenceTags.objects.filter(name_ru=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_ru=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_ru=hashtag)

                obj.tags.add(tag.id)

        elif request.LANGUAGE_CODE == "uz":
            for hashtag in tags:
                if science.ConferenceTags.objects.filter(name_uz=hashtag).exists():
                    tag = science.ConferenceTags.objects.get(name_uz=hashtag)
                else:
                    tag = science.ConferenceTags.objects.create(name_uz=hashtag)

                obj.tags.add(tag.id)

        obj.save()
        return HttpResponseRedirect(self.success_url)


class PendingConferenceDelete(custom.CustomDeleteView):
    model = science.PendingConference
    success_url = reverse_lazy("science:pending-conference-list")


class ConferenceTagsCreate(custom.CustomCreateView):
    model = science.ConferenceTags
    form_class = forms.ConferenceTagsForm
    template_name = "back/science/pending_conference/conference_tags_create.html"
    success_url = reverse_lazy("science:conference-tags-list")


class ConferenceTagsUpdate(UpdateView):
    model = science.ConferenceTags
    form_class = forms.ConferenceTagsForm
    context_object_name = "object"
    template_name = "back/science/pending_conference/conference_tags_update.html"
    success_url = reverse_lazy("science:conference-tags-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.name_uz = data["name_uz"]
        obj.name_ru = data["name_ru"]
        obj.name_en = data["name_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ConferenceTagsList(custom.CustomListView):
    model = science.ConferenceTags
    template_name = "back/science/pending_conference/conference_tags_list.html"
    queryset = model.objects.all()


class ConferenceTagsDelete(custom.CustomDeleteView):
    model = science.ConferenceTags
    success_url = reverse_lazy("science:conference-tags-list")


class ConferenceApplicationList(custom.CustomListView):
    model = science.ConferenceApplication
    template_name = "back/science/conference_application/conference_application_list.html"
    queryset = model.objects.all()


class ConferenceApplicationDelete(custom.CustomDeleteView):
    model = science.ConferenceApplication
    success_url = reverse_lazy("science:conference-application-list")


class ConferenceApplicationUpdate(UpdateView):
    model = science.ConferenceApplication
    form_class = forms.ConferenceApplicationForm
    context_object_name = "object"
    template_name = "back/science/conference_application/conference_application_update.html"
    success_url = reverse_lazy("science:conference-application-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConferenceApplicationUpdate, self).get_context_data(object_list=None, **kwargs)
        context["status"] = [
            ("pending", "Jarayonda"),
            ("accepted", "Ko'rildi"),
            ("rejected", "Rad etildi"),
        ]
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        print(data)
        obj.status = data["status"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


# Conference
class ConferenceList(custom.CustomListView):
    model = science.Conference
    template_name = "back/science/conference/conference_list.html"
    queryset = model.objects.all()


class ConferenceCreate(custom.CustomCreateView):
    model = science.Conference
    template_name = "back/science/conference/conference_create.html"
    form_class = forms.ConferenceForm
    success_url = reverse_lazy("science:conference-list")


class ConferenceUpdate(UpdateView):
    model = science.Conference
    form_class = forms.ConferenceForm
    context_object_name = "object"
    template_name = "back/science/conference/conference_update.html"
    success_url = reverse_lazy("science:conference-list")

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ConferenceDelete(custom.CustomDeleteView):
    model = science.Conference
    success_url = reverse_lazy("science:conference-list")


# ConferenceSubject
class ConferenceSubjectList(custom.CustomListView):
    model = science.ConferenceSubject
    template_name = "back/science/conference/section_list.html"
    queryset = model.objects.all()


class ConferenceSubjectCreate(CreateView):
    model = science.ConferenceSubject
    template_name = "back/science/conference/section_create.html"
    form_class = forms.ConferenceSubjectForm
    success_url = reverse_lazy("science:conference-subject-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConferenceSubjectCreate, self).get_context_data(object_list=object_list, **kwargs)
        context["conferences"] = science.Conference.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        if data.get("conference"):
            data["conference"] = science.Conference.objects.get(id=int(data["conference"]))

        obj = self.model.objects.create(**data)

        # obj.title_uz = data['title_uz']
        # obj.title_ru = data['title_ru']
        # obj.title_en = data['title_en']
        # obj.article = data['article']
        # obj.order = data['order']
        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ConferenceSubjectUpdate(UpdateView):
    model = science.ConferenceSubject
    form_class = forms.ConferenceSubjectForm
    context_object_name = "object"
    template_name = "back/science/conference/section_update.html"
    success_url = reverse_lazy("science:conference-subject-list")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ConferenceSubjectUpdate, self).get_context_data(object_list=object_list, **kwargs)
        context["conferences"] = science.Conference.objects.all()
        if not self.request.user.is_superuser:
            context["staff"] = CustomUser.objects.get(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST.dict()
        del data["csrfmiddlewaretoken"]
        obj = self.model.objects.get(id=self.kwargs["pk"])
        if data.get("conference"):
            data["conference"] = science.Conference.objects.get(id=int(data["conference"]))

        obj.title_uz = data["title_uz"]
        obj.title_ru = data["title_ru"]
        obj.title_en = data["title_en"]
        obj.department_uz = data["department_uz"]
        obj.department_en = data["department_en"]
        obj.department_ru = data["department_ru"]
        obj.conference = data["conference"]
        obj.place = data["place"]
        obj.start_date = data["start_date"]
        obj.end_date = data["end_date"]

        file = request.FILES.get("file")
        if file:
            obj.file = file

        obj.save()
        return HttpResponseRedirect(self.success_url)


class ConferenceSubjectDelete(custom.CustomDeleteView):
    model = science.ConferenceSubject
    success_url = reverse_lazy("science:conference-subject-list")
