from django.forms import ModelForm
from admin_panel.model import service


class ServiceForm(ModelForm):
    class Meta:
        model = service.Service
        fields = "__all__"
