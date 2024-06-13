from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import TestAnswerFactory


class TestQuestionListTestCase(APITestCase):
    def setUp(self) -> None:
        self.obj = TestAnswerFactory.create(is_correct=True)
        self.obj2 = TestAnswerFactory.create(is_correct=False)

    def test_list(self):
        url = reverse_lazy("syllabus:CheckTestAnswer", kwargs={"pk": self.obj.id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.data["is_correct"])

    def test_list2(self):
        url = reverse_lazy("syllabus:CheckTestAnswer", kwargs={"pk": self.obj2.id})
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(response.data["is_correct"])
