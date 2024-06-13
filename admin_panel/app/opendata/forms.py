from django.forms import ModelForm

from admin_panel.model import activity


class OpendataForm(ModelForm):
    class Meta:
        model = activity.Opendata
        fields = "__all__"
