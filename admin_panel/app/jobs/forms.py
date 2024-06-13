from django.forms import ModelForm

from admin_panel.model import activity


class LibdaryForm(ModelForm):
    class Meta:
        model = activity.Job
        fields = "__all__"
