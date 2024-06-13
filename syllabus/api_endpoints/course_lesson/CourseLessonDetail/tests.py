from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import CourseLessonFactory


class CourseLessonDetailTestCase(APITestCase):
    def setUp(self) -> None:
        self.course_lesson = CourseLessonFactory.create()

    def test_get_course_lesson_detail(self):
        url = reverse_lazy("syllabus:CourseLessonDetail", kwargs={"pk": self.course_lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
