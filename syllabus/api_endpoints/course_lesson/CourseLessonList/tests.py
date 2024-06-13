from django.urls import reverse_lazy
from rest_framework.test import APITestCase


class CourseSyllabusListTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_get_course_syllabus_list(self):
        url = reverse_lazy("syllabus:CourseLessonList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
