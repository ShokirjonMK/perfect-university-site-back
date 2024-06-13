from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.template import loader
from django.utils.translation import gettext_lazy as _
from typing_extensions import Self

from config.helpers import generate_unique_slug
from hr.models import BaseModel


class Syllabus(BaseModel):
    department = models.ForeignKey("admin_panel.Department", on_delete=models.CASCADE, related_name="syllabuses")
    title = models.CharField(verbose_name=_("Title"), max_length=255, null=True, blank=True)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = _("Department Syllabus")
        verbose_name_plural = _("Department Syllabuses")

    def save(self, *args, **kwargs):
        if self.title is None:
            self.title = self.department.title
            if self.slug is None:
                self.slug = generate_unique_slug(Syllabus, self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.title is None:
            return self.department.title
        return self.title


class SyllabusLanguage(BaseModel):
    name = models.CharField(verbose_name=_("Name"), max_length=255)
    language_code = models.CharField(verbose_name=_("Language code"), max_length=10)

    class Meta:
        verbose_name = _("Syllabus language")
        verbose_name_plural = _("Syllabus languages")

    def __str__(self):
        return self.name + " (" + self.language_code + ")"


class CourseYear(BaseModel):
    year = models.IntegerField(verbose_name=_("Year"), unique=True)

    class Meta:
        verbose_name = _("Course year")
        verbose_name_plural = _("Course years")

    def __str__(self):
        return str(self.year)


class CourseSyllabus(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    slug = models.SlugField(verbose_name=_("Title"), max_length=255, blank=True, null=True)
    direction = models.ForeignKey("admin_panel.Direction", on_delete=models.CASCADE, related_name="course_syllabuses")
    teacher = models.ForeignKey("admin_panel.CustomUser", on_delete=models.CASCADE, related_name="course_syllabuses")
    language = models.ForeignKey("SyllabusLanguage", on_delete=models.CASCADE, related_name="course_syllabuses")
    year = models.ForeignKey("CourseYear", on_delete=models.CASCADE, related_name="course_syllabuses")
    syllabus = models.ForeignKey(
        to="Syllabus", verbose_name=_("Department Syllabus"), on_delete=models.CASCADE, related_name="course_syllabuses"
    )

    class Meta:
        verbose_name = _("Syllabus")
        verbose_name_plural = _("Syllabuses")

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = generate_unique_slug(CourseSyllabus, self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CourseSyllabusInformation(BaseModel):
    class TypeTextChoices(models.TextChoices):
        information_about_science = "information_about_science", _("Information about science")
        location_of_science_classes = "location_of_science_classes", _("Location of science classes")
        information_about_teacher = "information_about_teacher", _("Information about teacher")

    type = models.CharField(verbose_name=_("Type"), max_length=255, choices=TypeTextChoices.choices)
    text = RichTextUploadingField(verbose_name=_("Text"), null=True, blank=True)
    course_syllabus = models.ForeignKey(
        "CourseSyllabus", on_delete=models.CASCADE, related_name="course_syllabus_informations"
    )

    class Meta:
        verbose_name = _("Course syllabus information")
        verbose_name_plural = _("Course syllabus information")
        unique_together = ("type", "course_syllabus")

    def __str__(self):
        return self.type


class CourseSyllabusTextSection(BaseModel):
    class TypeTextChoices(models.TextChoices):
        s_1_science_description = "1_science_description", _("1. Science description")
        s_2_purpose_of_science = "2_purpose_of_science", _("2. The Purpose of science")
        s_3_learning_outcomes = "3_results_of_education", _("3. Results of Education")
        s_4_teaching_methods = "4_teaching_methods", _("4. Teaching methods")
        s_5_assessment_methods = "5_assessment_methods", _("5. Assessment of Student Knowledge")
        s_6_academic_requirements = "6_academic_requirements", _("6. Academic requirements")
        s_7_independent_study = "7_independent_study", _("7. Independent education and Independent work")

    type = models.CharField(verbose_name=_("Type"), max_length=255, choices=TypeTextChoices.choices)
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    text = RichTextUploadingField(
        verbose_name=_("Text"),
        null=True,
        help_text=f"if you choose {TypeTextChoices.s_5_assessment_methods.label} "
        f"type, you can use {settings.PROCEDURE_ASSESSMENT_KEY} key for procedure assessment table",
        blank=True,
    )
    course_syllabus = models.ForeignKey(
        verbose_name=_("CourseSyllabus"),
        to="CourseSyllabus",
        on_delete=models.CASCADE,
        related_name="course_syllabus_text_sections",
    )

    class Meta:
        verbose_name = _("Course syllabus text section")
        verbose_name_plural = _("Course syllabus text sections")
        unique_together = ("type", "course_syllabus")

    def set_procedure_assessment_table(self):
        if self.type == CourseSyllabusTextSection.TypeTextChoices.s_5_assessment_methods:
            if self.text is not None:
                self.text: str
                context = StudentAssessment.objects.filter(course_syllabus=self.course_syllabus).procedure_assessment()
                html_response = loader.render_to_string("syllabus/procedure_assessment_list.html", context)
                self.text = self.text.replace(settings.PROCEDURE_ASSESSMENT_KEY, html_response)
                return True
        return False

    def save(self, *args, **kwargs):
        self.set_procedure_assessment_table()
        super().save(*args, **kwargs)


class CourseLesson(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    lesson_goals = models.TextField(verbose_name=_("Lecture goals"))
    course_syllabus = models.ForeignKey("CourseSyllabus", on_delete=models.CASCADE, related_name="course_lessons")
    order = models.IntegerField(verbose_name=_("list order"))

    class Meta:
        verbose_name = _("Course lesson")
        verbose_name_plural = _("Course lessons")

    def __str__(self):
        return self.title


class CourseLessonResourceTypeTextChoices(models.TextChoices):
    lecture = "lecture", _("Lecture")
    video = "video", _("Video")
    file = "file", _("File")
    url = "url", _("URL")


class CourseLessonResource(BaseModel):
    course_lesson = models.ForeignKey(
        "CourseLesson",
        verbose_name=_("Course lesson"),
        on_delete=models.CASCADE,
        null=True,
        related_name="course_lesson_resource",
    )
    course_syllabus = models.ForeignKey(
        "CourseSyllabus",
        verbose_name=_("Course syllabus"),
        on_delete=models.CASCADE,
        related_name="course_lesson_resource",
    )

    type = models.CharField(verbose_name=_("Type"), max_length=255, choices=CourseLessonResourceTypeTextChoices.choices)

    title = models.CharField(verbose_name=_("Title"), max_length=255)
    file_name = models.CharField(verbose_name=_("File name"), max_length=255, blank=True, null=True)
    file = models.FileField(verbose_name=_("File"), upload_to="course_lesson_videos", blank=True, null=True)
    file_size = models.IntegerField(verbose_name=_("File size"), default=0)
    order = models.IntegerField(verbose_name=_("List order"))
    url = models.URLField(verbose_name=_("URL"), blank=True, null=True)

    class Meta:
        verbose_name = _("Course lesson resource")
        verbose_name_plural = _("Course lesson resources")

    class ResourceQuerySet(models.QuerySet):
        default_type: CourseLessonResourceTypeTextChoices = None

        def filter(self, *args, **kwargs) -> Self:
            return super().filter(*args, **kwargs)

        def filter_by_type(self):
            if self.default_type is None:
                raise ValueError("Default type is not set")
            return self.filter(type=self.default_type)

    objects = ResourceQuerySet.as_manager()

    def set_course_syllabus(self):
        if self.course_lesson is not None:
            self.course_syllabus = self.course_lesson.course_syllabus

    def save(self, *args, **kwargs):
        self.set_course_syllabus()
        super().save(*args, **kwargs)

    def clean(self):
        if (self.file is not None and self.file.__str__() != "") and self.url is not None:
            raise ValidationError("You can't set both file and url")

    def __str__(self):
        return f"CourseLessonResource {self.type}"


class CourseLessonResourceSingleFile(BaseModel):
    file = models.FileField(verbose_name=_("File"), upload_to="course_lesson_resource_files", blank=True, null=True)
    course_lesson_resource = models.ForeignKey(
        to="CourseLessonResource",
        verbose_name=_("Course lesson resource"),
        on_delete=models.CASCADE,
        related_name="files",
    )

    class Meta:
        verbose_name = _("Course lesson resource single file")
        verbose_name_plural = _("Course lesson resource single files")


class CourseLessonResourceLecture(CourseLessonResource):
    class RecourseLectureQuerySet(CourseLessonResource.ResourceQuerySet):
        default_type = CourseLessonResourceTypeTextChoices.lecture

    objects = RecourseLectureQuerySet.as_manager()

    class Meta:
        verbose_name = _("Course lesson lecture")
        verbose_name_plural = _("Course lesson lectures")
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CourseLessonResourceTypeTextChoices.lecture
        super().save(*args, **kwargs)


class CourseLessonResourceVideo(CourseLessonResource):
    class RecourseVideoQuerySet(CourseLessonResource.ResourceQuerySet):
        default_type = CourseLessonResourceTypeTextChoices.video

    objects = RecourseVideoQuerySet.as_manager()

    class Meta:
        verbose_name = _("Course lesson video")
        verbose_name_plural = _("Course lesson videos")
        proxy = True

    def save(self, *args, **kwargs):
        self.type = CourseLessonResourceTypeTextChoices.video
        super().save(*args, **kwargs)


class CourseLessonResourceFile(CourseLessonResource):
    class RecourseFileQuerySet(CourseLessonResource.ResourceQuerySet):
        default_type = CourseLessonResourceTypeTextChoices.file

    objects = RecourseFileQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.type = CourseLessonResourceTypeTextChoices.file
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Course lesson file")
        verbose_name_plural = _("Course lesson files")
        proxy = True


class CourseLessonResourceUrl(CourseLessonResource):
    class RecourseUrlQuerySet(CourseLessonResource.ResourceQuerySet):
        default_type = CourseLessonResourceTypeTextChoices.url

    objects = RecourseUrlQuerySet.as_manager()

    def save(self, *args, **kwargs):
        self.type = CourseLessonResourceTypeTextChoices.url
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Course lesson url")
        verbose_name_plural = _("Course lesson urls")
        proxy = True


class CourseLessonHour(BaseModel):
    class TypeTextChoices(models.TextChoices):
        lecture = "lecture", _("Lecture")
        laboratory = "laboratory", _("Laboratory")
        practice = "practice", _("Practice")
        exam = "exam", _("Exam")
        independent_education = "independent_education", _("Independent Education")

    type = models.CharField(verbose_name=_("Type"), max_length=255, choices=TypeTextChoices.choices)
    lesson = models.ForeignKey("CourseLesson", on_delete=models.CASCADE, related_name="course_lesson_hours")
    hour = models.IntegerField(verbose_name=_("Hour"))

    class Meta:
        verbose_name = _("Course lesson hour")
        verbose_name_plural = _("Course lesson hours")
        unique_together = ("type", "lesson")

    def __str__(self):
        return f"{self.type} {self.hour}"


class CourseSyllabusTest(BaseModel):
    title = models.CharField(verbose_name=_("Title"), max_length=255)
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, null=True, blank=True)
    course_syllabus = models.OneToOneField(
        "CourseSyllabus", on_delete=models.CASCADE, related_name="course_syllabus_test"
    )

    class Meta:
        verbose_name = _("Syllabus test")
        verbose_name_plural = _("Syllabus tests")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = generate_unique_slug(CourseSyllabusTest, self.title)
        super().save(*args, **kwargs)


class TestQuestion(BaseModel):
    test = models.ForeignKey("CourseSyllabusTest", on_delete=models.CASCADE, related_name="test_questions")
    question = RichTextUploadingField(verbose_name=_("Question"))

    class Meta:
        verbose_name = _("Test question")
        verbose_name_plural = _("Test questions")

    def __str__(self):
        return f"{self.id} {self.question}"


class TestAnswer(BaseModel):
    question = models.ForeignKey("TestQuestion", on_delete=models.CASCADE, related_name="test_answers")
    answer = models.CharField(verbose_name=_("Answer"), max_length=255)
    is_correct = models.BooleanField(verbose_name=_("Is correct"))

    class Meta:
        verbose_name = _("Test answer")
        verbose_name_plural = _("Test answers")
        constraints = [
            models.UniqueConstraint(
                fields=["question", "is_correct"],
                condition=models.Q(is_correct=True),
                name="%(app_label)s_%(class)s_unique_correct_question_answer",
            )
        ]


class StudentAssessmentQueryset(models.QuerySet):
    def filter(self, *args, **kwargs) -> Self:
        return super().filter(*args, **kwargs)

    def procedure_assessment(self):
        return {
            "headers": [
                _("Rating Assessment types"),
                _("Max. Ball"),
                _("Task to be Completed"),
                _("Task Completion Time"),
            ],
            "object_list": self,
            "total": {
                "name": _("Total"),
                "max_ball": self.aggregate(total_max_ball=models.Sum("max_ball")).get("total_max_ball", 0),
            },
        }


class StudentAssessment(models.Model):
    course_syllabus = models.ForeignKey("CourseSyllabus", on_delete=models.CASCADE, related_name="student_assessments")
    rating_assessment = models.CharField(
        max_length=3000,
    )
    max_ball = models.IntegerField()
    task_to_be_completed = RichTextUploadingField()
    task_completion_time = RichTextUploadingField(null=True, blank=True)
    order = models.IntegerField()

    objects = StudentAssessmentQueryset.as_manager()

    def __str__(self):
        return self.rating_assessment

    class Meta:
        verbose_name = _("Student assessment")
        verbose_name_plural = _("Student assessments")
