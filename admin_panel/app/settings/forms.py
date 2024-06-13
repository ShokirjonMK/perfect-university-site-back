from django.forms import ModelForm

from admin_panel.model.settings import MainPageSetting, Slider, TopLink, Sidebar


class GeneralSettingForm(ModelForm):
    class Meta:
        model = MainPageSetting
        fields = "__all__"


class SliderForm(ModelForm):
    class Meta:
        model = Slider
        fields = "__all__"


class TopLinkForm(ModelForm):
    class Meta:
        model = TopLink
        fields = "__all__"


class SidebarForm(ModelForm):
    class Meta:
        model = Sidebar
        fields = "__all__"
