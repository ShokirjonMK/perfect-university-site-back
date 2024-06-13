from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import CourseSyllabusTestFactory, CourseSyllabusFactory


class TestQuestionListTestCase(APITestCase):
    def setUp(self) -> None:
        self.course_syllabus = CourseSyllabusFactory.create()
        self.course_syllabus_test = CourseSyllabusTestFactory.create(course_syllabus=self.course_syllabus)

    def test_list(self):
        url = reverse_lazy("syllabus:SyllabusTestList", kwargs={"syllabus_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())

    def test_slug_list(self):
        url = reverse_lazy("syllabus:SyllabusTestSlugList", kwargs={"syllabus_slug": self.course_syllabus.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
