from django.forms import ModelForm
from admin_panel.model import international
from admin_panel.model.international import Ranking


class GrantForm(ModelForm):
    class Meta:
        model = international.Grant
        fields = "__all__"


class GrantFilesForm(ModelForm):
    class Meta:
        model = international.GrantFiles
        fields = "__all__"


class InternationalConferencePageForm(ModelForm):
    class Meta:
        model = international.InternationalConferencePage
        fields = "__all__"


class InternationalRelationForm(ModelForm):
    class Meta:
        model = international.InternationalRelation
        fields = "__all__"


class InternationalStaffForm(ModelForm):
    class Meta:
        model = international.InternationalStaff
        fields = "__all__"


class InternationalUsufulLinkForm(ModelForm):
    class Meta:
        model = international.InternationalUsufulLink
        fields = "__all__"


class InternationalPartnerForm(ModelForm):
    class Meta:
        model = international.InternationalPartner
        fields = "__all__"


class InternationalFacultyApplicationForm(ModelForm):
    class Meta:
        model = international.InternationalFacultyApplication
        fields = "__all__"


class RankingForm(ModelForm):
    class Meta:
        model = Ranking
        fields = (
            "id",
            "reputation_ranking",
            "academic_reputation_ranking",
            "employer_reputation_ranking",
            "reputation_assessment",
            "image"
        )


class InternationalCooperationCategory(ModelForm):
    class Meta:
        model = international.InternationalCooperationCategory
        fields = ("id", "title", "slug")


class InternationalCooperationForm(ModelForm):
    class Meta:
        model = international.InternationalCooperation
        fields = (
            "id",
            "title",
            "content",
            "image",
            "link",
            "category"
        )
