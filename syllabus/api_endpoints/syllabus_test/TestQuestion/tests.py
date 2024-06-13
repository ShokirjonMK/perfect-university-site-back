from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import TestQuestionFactory, CourseSyllabusTestFactory, TestAnswerFactory


class TestQuestionListTestCase(APITestCase):
    def setUp(self) -> None:
        syllabus_test = CourseSyllabusTestFactory.create()
        syllabus_test_2 = CourseSyllabusTestFactory.create()
        self.question_1 = TestQuestionFactory.create_batch(
            4,
            test=syllabus_test,
        )
        self.question_2 = TestQuestionFactory.create_batch(
            4,
            test=syllabus_test_2,
        )
        for question in self.question_1:
            TestAnswerFactory.create_batch(4, question=question, is_correct=False)
        for question in self.question_2:
            TestAnswerFactory.create_batch(4, question=question, is_correct=False)

    def test_list(self):
        url = reverse_lazy("syllabus:TestQuestionList", kwargs={"test_id": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
