from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import StudentAssessmentFactory


class ProcedureAssessmentTestCase(APITestCase):
    def setUp(self) -> None:
        StudentAssessmentFactory.create_batch(10)

    def test_get_list(self):
        response = self.client.get(reverse_lazy("syllabus:ProcedureAssessmentList"))
        self.assertEqual(response.status_code, 200)
