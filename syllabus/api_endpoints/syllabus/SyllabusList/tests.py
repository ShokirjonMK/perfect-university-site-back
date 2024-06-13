from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import SyllabusFactory


class SyllabusListTest(APITestCase):
    def setUp(self) -> None:
        SyllabusFactory.create_batch(10)

    def test_list(self):
        url = reverse_lazy("syllabus:SyllabusList")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
