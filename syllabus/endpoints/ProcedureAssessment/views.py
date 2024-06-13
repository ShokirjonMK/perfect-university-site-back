from django.views.generic import ListView

from syllabus.models import StudentAssessment


class ProcedureAssessmentListTemplateView(ListView):
    def get_queryset(self):
        return StudentAssessment.objects.filter(course_syllabus_id=self.kwargs["syllabus_id"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.object_list.procedure_assessment())
        return context

    template_name = "syllabus/procedure_assessment_list.html"


__all__ = ["ProcedureAssessmentListTemplateView"]
