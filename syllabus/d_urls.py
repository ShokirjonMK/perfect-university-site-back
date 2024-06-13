from django.urls import path
from .endpoints import ProcedureAssessmentListTemplateView

app_name = "syllabus"

urlpatterns = [
    path(
        "ProcedureAssessmentListTemplateView/<int:syllabus_id>/",
        ProcedureAssessmentListTemplateView.as_view(),
        name="ProcedureAssessmentListTemplateView",
    ),
]
