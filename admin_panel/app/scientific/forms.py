from django.forms import ModelForm
from admin_panel.model.scientific import ScientificJournalDesc, ScientificJournal


class ScientificJournalDescForm(ModelForm):
    class Meta:
        model = ScientificJournalDesc
        fields = "__all__"


class ScientificJournalForm(ModelForm):
    class Meta:
        model = ScientificJournal
        fields = "__all__"
