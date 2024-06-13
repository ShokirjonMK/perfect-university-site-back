from django import forms
from django.forms import BaseInlineFormSet

from syllabus.models import TestAnswer, TestQuestion, CourseSyllabusTextSection, CourseLesson, CourseLessonHour
from django.utils.translation import gettext_lazy as _


class TestQuestionAdminForm(forms.ModelForm):
    class Meta:
        model = TestAnswer
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class TestAnswerAdminForm(forms.ModelForm):
    class Meta:
        model = TestAnswer
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        question: TestQuestion = cleaned_data.get("question")
        if cleaned_data["is_correct"]:
            question.test_answers.exclude(pk=self.instance.pk).update(is_correct=False)
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


class TestAnswerFormSet(BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()
        answer_cleaned_datas = []
        form: TestAnswerAdminForm
        for form in self.forms:
            if form.Meta.model == TestAnswer:
                answer_cleaned_datas.append(form.cleaned_data)
        true_answers = list(filter(lambda x: x["is_correct"] is True, answer_cleaned_datas))
        if len(true_answers) > 1:
            raise forms.ValidationError("There can be only one correct answer")
        return cleaned_data


class CourseSyllabusTextSectionForm(forms.ModelForm):
    class Meta:
        model = CourseSyllabusTextSection
        fields = "__all__"


class CourseLessonInlineForm(forms.ModelForm):
    lecture_hour = forms.IntegerField(help_text=_("Lecture hour"))
    laboratory_hour = forms.IntegerField(help_text=_("Laboratory hour"))
    practice_hour = forms.IntegerField(help_text=_("Practice hour"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.id:
            lecture_hour_cl = CourseLessonHour.objects.filter(
                lesson=self.instance, type=CourseLessonHour.TypeTextChoices.lecture
            ).first()
            if lecture_hour_cl is not None:
                self.fields["lecture_hour"].initial = lecture_hour_cl.hour
            laboratory_hour_cl = CourseLessonHour.objects.filter(
                lesson=self.instance, type=CourseLessonHour.TypeTextChoices.laboratory
            ).first()
            if laboratory_hour_cl is not None:
                self.fields["laboratory_hour"].initial = laboratory_hour_cl.hour
            practice_hour_cl = CourseLessonHour.objects.filter(
                lesson=self.instance, type=CourseLessonHour.TypeTextChoices.practice
            ).first()
            if practice_hour_cl is not None:
                self.fields["practice_hour"].initial = practice_hour_cl.hour

    class Meta:
        model = CourseLesson
        fields = "__all__"

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            lecture_hour = self.cleaned_data.get("lecture_hour")
            laboratory_hour = self.cleaned_data.get("laboratory_hour")
            practice_hour = self.cleaned_data.get("practice_hour")
            instance.save()
            CourseLessonHour.objects.get_or_create(
                type=CourseLessonHour.TypeTextChoices.lecture,
                lesson=instance,
                defaults = {
                    "hour": lecture_hour,
                }
            )
            CourseLessonHour.objects.get_or_create(
                type=CourseLessonHour.TypeTextChoices.laboratory,
                lesson=instance,
                defaults={
                    "hour": laboratory_hour,
                }
            )
            CourseLessonHour.objects.get_or_create(
                type=CourseLessonHour.TypeTextChoices.practice,
                lesson=instance,
                defaults={
                    "hour": practice_hour,
                }
            )
        return instance
