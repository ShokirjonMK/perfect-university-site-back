from django.test import TestCase

from .factories import CourseSyllabusTextSectionFactory


class SyllabusTest(TestCase):
    def test_syllabus(self):
        CourseSyllabusTextSectionFactory.create()
