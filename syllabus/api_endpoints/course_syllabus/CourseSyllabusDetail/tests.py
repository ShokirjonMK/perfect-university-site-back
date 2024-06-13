from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from syllabus.factories import (
    CourseSyllabusFactory,
    CourseSyllabusTextSectionFactory,
    CourseSyllabusInformationFactory,
    CourseSyllabusTestFactory,
)
from syllabus.models import CourseSyllabusTextSection, CourseSyllabusInformation


class CourseSyllabusDetailTestCase(APITestCase):
    def setUp(self) -> None:
        self.course_syllabus = CourseSyllabusFactory.create()
        # section_1 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_1_science_description,
            course_syllabus=self.course_syllabus,
        )
        # section_2 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_2_purpose_of_science,
            course_syllabus=self.course_syllabus,
        )
        # section_3 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_3_learning_outcomes,
            course_syllabus=self.course_syllabus,
        )
        # section_4 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_4_teaching_methods,
            course_syllabus=self.course_syllabus,
        )
        # section_5 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_5_assessment_methods,
            course_syllabus=self.course_syllabus,
        )
        # section_6 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_6_academic_requirements,
            course_syllabus=self.course_syllabus,
        )
        # section_7 =
        CourseSyllabusTextSectionFactory.create(
            type=CourseSyllabusTextSection.TypeTextChoices.s_7_independent_study,
            course_syllabus=self.course_syllabus,
        )

        CourseSyllabusInformationFactory.create(
            course_syllabus=self.course_syllabus,
            type=CourseSyllabusInformation.TypeTextChoices.information_about_science,
        )
        CourseSyllabusInformationFactory.create(
            course_syllabus=self.course_syllabus,
            type=CourseSyllabusInformation.TypeTextChoices.information_about_teacher,
        )
        CourseSyllabusInformationFactory.create(
            course_syllabus=self.course_syllabus,
            type=CourseSyllabusInformation.TypeTextChoices.location_of_science_classes,
        )
        CourseSyllabusTestFactory.create(
            course_syllabus=self.course_syllabus,
        )

    def test_get_course_syllabus_detail(self):
        url = reverse_lazy("syllabus:CourseSyllabusDetail", kwargs={"pk": self.course_syllabus.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_course_syllabus_slug_detail(self):
        url = reverse_lazy("syllabus:CourseSyllabusSlugDetail", kwargs={"slug": self.course_syllabus.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
