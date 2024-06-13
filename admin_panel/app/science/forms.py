from django.forms import ModelForm
from admin_panel.model import science


class NewsForm(ModelForm):
    class Meta:
        model = science.ScienceNews
        fields = "__all__"


class ScienceCenterForm(ModelForm):
    class Meta:
        model = science.ScienceCenter
        fields = "__all__"


class NewsCategoryForm(ModelForm):
    class Meta:
        model = science.ScienceNewsCategory
        fields = "__all__"


class NewsHashtagForm(ModelForm):
    class Meta:
        model = science.ScienceNewsHashtag
        fields = "__all__"


class ConferenceTagsForm(ModelForm):
    class Meta:
        model = science.ConferenceTags
        fields = "__all__"


class ConferenceApplicationForm(ModelForm):
    class Meta:
        model = science.ConferenceApplication
        fields = "__all__"


class NewsFileForm(ModelForm):
    class Meta:
        model = science.ScienceFiles
        fields = "__all__"


class SeminarForm(ModelForm):
    class Meta:
        model = science.Seminar
        fields = "__all__"


class SeminarCategoryForm(ModelForm):
    class Meta:
        model = science.SeminarCategory
        fields = "__all__"


class SeminarHashtagForm(ModelForm):
    class Meta:
        model = science.SeminarHashtag
        fields = "__all__"


class MonoArticleForm(ModelForm):
    class Meta:
        model = science.MonoArticle
        fields = "__all__"


class MonoFilesForm(ModelForm):
    class Meta:
        model = science.MonoFiles
        fields = "__all__"


class MonoSectionForm(ModelForm):
    class Meta:
        model = science.Section
        fields = "__all__"


class ConferenceForm(ModelForm):
    class Meta:
        model = science.Conference
        fields = "__all__"


class PendingConferenceForm(ModelForm):
    class Meta:
        model = science.PendingConference
        fields = "__all__"


class ConferenceSubjectForm(ModelForm):
    class Meta:
        model = science.ConferenceSubject
        fields = "__all__"
