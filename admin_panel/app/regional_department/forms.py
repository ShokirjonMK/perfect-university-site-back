from django.forms import ModelForm

from admin_panel.model import ministry


class RegionalDepartmentForm(ModelForm):
    class Meta:
        model = ministry.RegionalDepartment
        fields = "__all__"
