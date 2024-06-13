from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import SyllabusFactory


class SyllabusDetailTest(APITestCase):
    def setUp(self) -> None:
        self.syllabus = SyllabusFactory.create()

    def test_detail(self):
        url = reverse_lazy("syllabus:SyllabusDetail", kwargs={"pk": self.syllabus.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_slug_detail(self):
        url = reverse_lazy("syllabus:SyllabusDetailSlug", kwargs={"slug": self.syllabus.slug})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
