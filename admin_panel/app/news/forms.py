from django import forms
from django.forms import ModelForm

from admin_panel.model import press_service as news


class NewsForm(ModelForm):
    class Meta:
        model = news.News
        fields = "__all__"


class ObjectiveForm(ModelForm):
    class Meta:
        model = news.Objective
        fields = ("number", "slug", "color", "icon", "title_uz", "title_ru", "title_en", "description_uz",
                  "description_ru", "description_en")

    def clean_number(self):
        number = self.cleaned_data.get("number")

        if number <= 0:
            raise forms.ValidationError("Number must be a positive integer.")

        if news.Objective.objects.filter(number=number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Number must be unique.")

        return number


# class ElonlarForm(ModelForm):
#     class Meta:
#         model = news.Elonlar
#         fields = '__all__'


class NewsCategoryForm(ModelForm):
    class Meta:
        model = news.NewsCategory
        fields = "__all__"


class NewsHashtagForm(ModelForm):
    class Meta:
        model = news.NewsHashtag
        fields = "__all__"


class FAQForm(ModelForm):
    class Meta:
        model = news.FAQ
        fields = "__all__"
