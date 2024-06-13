from django.db import models
from django.utils.translation import gettext_lazy as _

from admin_panel.common import generate_field
from config import settings

from ckeditor.fields import RichTextField


class Quizz(models.Model):
    title = models.CharField(max_length=500)
    is_published = models.BooleanField(default=False)
    main_page = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "quizz"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def result_count(self):
        return QuestionResult.objects.filter(quizz=self).count()

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Quizz, self).save(*args, **kwargs)


class Question(models.Model):
    title = models.CharField(max_length=500)
    quizz = models.ForeignKey("Quizz", on_delete=models.CASCADE, related_name="question", null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    class Meta:
        db_table = "question"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def percentage(self):
        if self.quizz and self.quizz.result_count > 0:
            overall = 100 / self.quizz.result_count
            obj = self.count * overall
            return int(obj)
        return 0

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(Question, self).save(*args, **kwargs)


class QuestionResult(models.Model):
    # user = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="result")
    quizz = models.ForeignKey(Quizz, on_delete=models.CASCADE, related_name="result")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "question_result"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.quizz)


STATUS = (
    (0, _("Jarayonda")),
    (1, _("Ko'rildi")),
    (2, _("Rad etildi")),
)


class Application(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=30)
    email = models.EmailField(null=True, blank=True)
    file = models.FileField(upload_to="Application", null=True, blank=True)
    phone_number = models.CharField(max_length=9)
    status = models.IntegerField(choices=STATUS, default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # date = models.DateField(auto_now_add=True)
    application_text = RichTextField()

    class Meta:
        db_table = "application"
        ordering = ("-created_at",)

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None
