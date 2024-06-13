from django.forms import ModelForm
from admin_panel.model import ministry
from admin_panel.model.international import Ranking
from admin_panel.model.static import OurMission, OurMissionItem, History, HistoryItem, HistoryYear
from ckeditor.widgets import CKEditorWidget


class AboutMinistryForm(ModelForm):
    class Meta:
        model = ministry.AboutMinistry
        fields = "__all__"


class GoalForm(ModelForm):
    class Meta:
        model = ministry.Goal
        fields = "__all__"


class StructureForm(ModelForm):
    class Meta:
        model = ministry.Structure
        fields = "__all__"


class DepartmentForm(ModelForm):
    class Meta:
        model = ministry.Department
        fields = "__all__"


class OrganizationForm(ModelForm):
    class Meta:
        model = ministry.Organization
        fields = "__all__"


class StaffForm(ModelForm):
    class Meta:
        model = ministry.Staff
        fields = "__all__"


class OurMissionForm(ModelForm):
    class Meta:
        model = OurMission
        fields = ("id", "title", "description", "image", "is_main")


class OurMissionItemForm(ModelForm):
    class Meta:
        model = OurMissionItem
        fields = ("id", "title", "our_mission")


class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ("id", "title", "description", "order")


class HistoryItemForm(ModelForm):
    class Meta:
        model = HistoryItem
        fields = ("id", "content", "history")


class HistoryYearForm(ModelForm):
    class Meta:
        model = HistoryYear
        fields = ("id", "year", "title", "description", "history")


class FamousGraduateForm(ModelForm):
    class Meta:
        model = ministry.FamousGraduate
        fields = "__all__"


class CouncilStaffForm(ModelForm):
    class Meta:
        model = ministry.CouncilStaff
        fields = "__all__"


class CouncilForm(ModelForm):
    class Meta:
        model = ministry.Council
        fields = "__all__"
        exclude = ["title", "content"]


class NightProgramForm(ModelForm):
    class Meta:
        model = ministry.NightProgram
        fields = "__all__"


class StudyProgramForm(ModelForm):
    class Meta:
        model = ministry.StudyProgram
        fields = "__all__"


class ForeignStudentForm(ModelForm):
    class Meta:
        model = ministry.ForeignStudent
        fields = ("id", "background_image", "youtube_link")


class KafedraForm(ModelForm):
    class Meta:
        model = ministry.Kafedra
        fields = "__all__"


class UstavForm(ModelForm):
    class Meta:
        model = ministry.Ustav
        fields = "__all__"


class UnversityFileForm(ModelForm):
    class Meta:
        model = ministry.UnversityFile
        fields = "__all__"
