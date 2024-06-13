from django.forms import ModelForm

from admin_panel.model import vacancies


class VacancyForm(ModelForm):
    class Meta:
        model = vacancies.Form
        fields = "__all__"


class PositionForm(ModelForm):
    class Meta:
        model = vacancies.Position
        fields = "__all__"


class VacantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(VacantForm, self).__init__(*args, **kwargs)
        self.fields["status"].widget.attrs = {"class": "form-control"}

    class Meta:
        model = vacancies.Vacant
        fields = ["status"]
