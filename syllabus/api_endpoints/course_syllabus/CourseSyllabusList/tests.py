from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import CourseSyllabusFactory


class SyllabusListTest(APITestCase):
    def setUp(self) -> None:
        CourseSyllabusFactory.create_batch(10)

    def test_list(self):
        url = reverse_lazy("syllabus:CourseSyllabusList")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
