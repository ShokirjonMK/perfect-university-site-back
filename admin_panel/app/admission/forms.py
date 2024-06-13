from django.forms import ModelForm
from admin_panel.model.courses import Admission


class AdmissionForm(ModelForm):
    class Meta:
        model = Admission
        fields = "__all__"
