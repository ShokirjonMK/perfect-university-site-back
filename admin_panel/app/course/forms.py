from django.forms import ModelForm, CheckboxSelectMultiple, MultipleChoiceField

from admin_panel.model import courses
from admin_panel.model.international import ExternalSection


class CourseCatalogForm(ModelForm):
    class Meta:
        model = courses.CourseCatalog
        fields = "__all__"


class DirectionForm(ModelForm):
    education_types = MultipleChoiceField(
        widget=CheckboxSelectMultiple,
        choices=courses.EducationType.choices,
        required=False,
    )

    class Meta:
        model = courses.Direction
        fields = "__all__"


class RatingSystemForm(ModelForm):
    class Meta:
        model = courses.RatingSystem
        fields = "__all__"


class QualificationRequirementsForm(ModelForm):
    class Meta:
        model = courses.QualificationRequirement
        fields = "__all__"


class CurriculumForm(ModelForm):
    class Meta:
        model = courses.Curriculum
        fields = "__all__"


class EntrantPageForm(ModelForm):
    class Meta:
        model = courses.EntrantPage
        fields = "__all__"


class EntrantPageFileForm(ModelForm):
    class Meta:
        model = courses.EntrantPageFile
        fields = "__all__"


class EntrantPageQuestionForm(ModelForm):
    class Meta:
        model = courses.EntrantPageQuestion
        fields = "__all__"


# Sirtqi bo'lim formasi
class ExternalSectionPageForm(ModelForm):
    class Meta:
        model = ExternalSection
        fields = "__all__"
