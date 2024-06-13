import factory
from django.contrib.auth.models import User
from factory.django import DjangoModelFactory
from faker import Factory as FakerFactory

from admin_panel.model.ministry import Department
from admin_panel.model.user import CustomUser
from admin_panel.model.courses import Direction
from .models import (
    Syllabus,
    SyllabusLanguage,
    CourseYear,
    CourseSyllabus,
    CourseSyllabusInformation,
    CourseSyllabusTextSection,
    CourseLesson,
    CourseLessonResource,
    CourseLessonResourceTypeTextChoices,
    CourseLessonResourceVideo,
    CourseLessonResourceFile,
    CourseLessonResourceUrl,
    CourseLessonHour,
    CourseSyllabusTest,
    TestQuestion,
    TestAnswer,
    StudentAssessment,
)

faker = FakerFactory.create()


class DirectionFactory(DjangoModelFactory):
    class Meta:
        model = Direction

    title = factory.Faker("text", max_nb_chars=255)
    shifr = factory.Faker("text", max_nb_chars=32)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    is_staff = factory.Faker("boolean")
    is_active = factory.Faker("boolean")
    date_joined = factory.Faker("date_time_this_decade")


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    user = factory.SubFactory(UserFactory)
    email = factory.Faker("email")
    phone = factory.Sequence(lambda n: f"+99890123{n}5{n}")
    image = factory.django.ImageField(color="blue")
    created_at = factory.Faker("date_time_this_year")
    updated_at = factory.Faker("date_time_this_month")


class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    title = factory.Faker("sentence", nb_words=3)
    image = factory.django.ImageField(color="blue")
    main_page = False
    description = factory.Faker("paragraph")

    kafedras = factory.Faker("paragraph")
    directions = factory.Faker("paragraph")
    history = factory.Faker("paragraph")
    study_works = factory.Faker("paragraph")
    spiritual_directions = factory.Faker("paragraph")
    research_works = factory.Faker("paragraph")
    innovative_works = factory.Faker("paragraph")
    faculty_innovative_works = factory.Faker("paragraph")
    cooperation = factory.Faker("paragraph")
    international_relations = factory.Faker("paragraph")
    faculty_international_relations = factory.Faker("paragraph")
    link = factory.Faker("url")


class SyllabusFactory(DjangoModelFactory):
    department = factory.SubFactory(DepartmentFactory)

    class Meta:
        model = Syllabus


class SyllabusLanguageFactory(DjangoModelFactory):
    class Meta:
        model = SyllabusLanguage

    name = factory.Sequence(lambda n: f"Language {n}")
    language_code = factory.Sequence(lambda n: f"lang{n}")


class CourseYearFactory(DjangoModelFactory):
    class Meta:
        model = CourseYear

    year = factory.Sequence(lambda n: n + 2000)


class CourseSyllabusFactory(DjangoModelFactory):
    class Meta:
        model = CourseSyllabus

    title = factory.Faker("sentence")
    slug = factory.Faker("slug")
    direction = factory.SubFactory(DirectionFactory)
    teacher = factory.SubFactory(CustomUserFactory)
    language = factory.SubFactory(SyllabusLanguageFactory)
    year = factory.SubFactory(CourseYearFactory)
    syllabus = factory.SubFactory(SyllabusFactory)


class CourseSyllabusInformationFactory(DjangoModelFactory):
    class Meta:
        model = CourseSyllabusInformation

    type = CourseSyllabusInformation.TypeTextChoices.information_about_science
    text = factory.Faker("paragraph")
    course_syllabus = factory.SubFactory(CourseSyllabusFactory)


class CourseSyllabusTextSectionFactory(DjangoModelFactory):
    class Meta:
        model = CourseSyllabusTextSection

    type = CourseSyllabusTextSection.TypeTextChoices.s_1_science_description
    title = factory.Faker("sentence")
    text = factory.Faker("paragraph")
    course_syllabus = factory.SubFactory(CourseSyllabusFactory)


class CourseLessonFactory(DjangoModelFactory):
    class Meta:
        model = CourseLesson

    title = factory.Faker("sentence")
    lesson_goals = factory.Faker("paragraph")
    course_syllabus = factory.SubFactory(CourseSyllabusFactory)
    order = factory.Sequence(lambda n: n)


class CourseLessonResourceFactory(DjangoModelFactory):
    class Meta:
        model = CourseLessonResource

    course_lesson = factory.SubFactory(CourseLessonFactory)
    course_syllabus = factory.SubFactory(CourseSyllabusFactory)
    type = CourseLessonResourceTypeTextChoices.video
    title = factory.Faker("word")
    file_name = factory.Faker("file_name")
    file_size = factory.Faker("random_int", min=100, max=100000)
    order = factory.Sequence(lambda n: n)


class CourseLessonResourceVideoFactory(CourseLessonResourceFactory):
    class Meta:
        model = CourseLessonResourceVideo


class CourseLessonResourceFileFactory(CourseLessonResourceFactory):
    class Meta:
        model = CourseLessonResourceFile


class CourseLessonResourceUrlFactory(CourseLessonResourceFactory):
    class Meta:
        model = CourseLessonResourceUrl


class CourseLessonHourFactory(DjangoModelFactory):
    class Meta:
        model = CourseLessonHour

    type = CourseLessonHour.TypeTextChoices.lecture
    lesson = factory.SubFactory(CourseLessonFactory)
    hour = factory.Faker("random_int", min=1, max=24)


class CourseSyllabusTestFactory(DjangoModelFactory):
    class Meta:
        model = CourseSyllabusTest

    title = factory.Faker("sentence")
    course_syllabus = factory.SubFactory(CourseSyllabusFactory)


class TestQuestionFactory(DjangoModelFactory):
    class Meta:
        model = TestQuestion

    test = factory.SubFactory(CourseSyllabusTestFactory)
    question = factory.Faker("paragraph")


class TestAnswerFactory(DjangoModelFactory):
    class Meta:
        model = TestAnswer

    question = factory.SubFactory(TestQuestionFactory)
    answer = factory.Faker("word")
    is_correct = factory.Faker("boolean")


class StudentAssessmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = StudentAssessment

    course_syllabus = factory.SubFactory(CourseSyllabusFactory)
    rating_assessment = factory.Faker("sentence")
    max_ball = factory.Faker("random_int", min=0, max=100)
    task_to_be_completed = factory.Faker("text")
    task_completion_time = factory.Faker("date_time")
    order = factory.Sequence(lambda n: n)
