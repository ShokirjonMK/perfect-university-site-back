from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import (
    CourseLessonResourceUrlFactory,
    CourseLessonResourceVideoFactory,
    CourseLessonResourceFileFactory,
)


class CourseResourceListTestCase(APITestCase):
    def setUp(self) -> None:
        pass

    def test_course_lesson_resource_url_list(self):
        CourseLessonResourceUrlFactory.create_batch(10)
        url = reverse_lazy("syllabus:CourseResourceLessonUrlList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_course_lesson_resource_video_list(self):
        CourseLessonResourceVideoFactory.create_batch(10)
        url = reverse_lazy("syllabus:CourseResourceLessonVideoList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_course_lesson_resource_file_list(self):
        CourseLessonResourceFileFactory.create_batch(10)
        url = reverse_lazy("syllabus:CourseResourceLessonFileList")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
