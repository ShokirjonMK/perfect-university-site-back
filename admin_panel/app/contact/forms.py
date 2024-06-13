from django.forms import ModelForm

from admin_panel.model import contact


class ContactForm(ModelForm):
    class Meta:
        model = contact.Contact
        fields = "__all__"
