from django.forms import ModelForm
from admin_panel.model import docs


class ReportForm(ModelForm):
    class Meta:
        model = docs.Report
        fields = "__all__"
