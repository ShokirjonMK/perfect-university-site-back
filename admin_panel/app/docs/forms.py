from django.forms import ModelForm
from admin_panel.model import docs


class DocsForm(ModelForm):
    class Meta:
        model = docs.Docs
        fields = "__all__"


class LawyerPageForm(ModelForm):
    class Meta:
        model = docs.LawyerPage
        fields = "__all__"
