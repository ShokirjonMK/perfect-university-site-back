from django.forms import ModelForm

from . import models


class VacancyForm(ModelForm):
    class Meta:
        model = models.Form
        fields = "__all__"


class PositionForm(ModelForm):
    class Meta:
        model = models.Position
        fields = "__all__"


class VacantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VacantForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs = {"class": "form-control"}

    class Meta:
        model = models.NewVacant
        fields = ["status"]


class LibdaryForm(ModelForm):
    class Meta:
        model = models.Job
        fields = "__all__"
