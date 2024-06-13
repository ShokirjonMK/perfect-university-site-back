import os.path

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from admin_panel.common import generate_field
from admin_panel.model.vacancies import Form

# Image cropping conf
THUMBNAIL = [160, 250]
IMAGE = [300, 300]


class Articles(models.Model):
    title = models.CharField(max_length=200, null=True)
    author = models.CharField(max_length=200, null=True)
    content = RichTextField()
    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "articles"
        ordering = ["-created_at"]
        verbose_name_plural = "Ilmiy maqola"

    def __str__(self):
        return str(self.title)

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return ""

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.author_uz:
            self.author_sr = generate_field(self.author_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        super(Articles, self).save(*args, **kwargs)


class ArticlesFiles(models.Model):
    articles = models.ForeignKey(Articles, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="articles")

    class Meta:
        db_table = "articles_files"
        ordering = ["-id"]

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return ""


class Opendata(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "opendata"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        # if self.content_uz:
        #     self.content_sr = generate_field(self.content_uz)

        super(Opendata, self).save(*args, **kwargs)


class OpenDataFiles(models.Model):
    opendata = models.ForeignKey(Opendata, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="opendata")

    class Meta:
        db_table = "opendata_files"
        ordering = ["-id"]

    def __str__(self):
        return self.file.name

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return ""

    @property
    def file_name(self):
        if self.file:
            return os.path.basename(self.file.name)


def generate_unique_slug(cls, field):
    origin_slug = slugify(field)
    unique_slug = origin_slug
    numb = 1
    while cls.objects.filter(slug=unique_slug).exists():
        unique_slug = "%s-%d" % (origin_slug, numb)
        numb += 1
    return unique_slug

class Job(models.Model):
    title = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200)
    content = RichTextField()
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, blank=True)
    # place = models.TextField()
    # reg_link = models.URLField(null=True, blank=True)
    salary = models.BigIntegerField(default=0)
    views = models.IntegerField(default=0)
    # photo = models.FileField(upload_to='job')
    is_published = models.BooleanField(default=False)

    date = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "job"
        ordering = ["-date"]

    def __str__(self):
        return str(self.title)

    # @property
    # def photo_url(self):
    #     # "Returns the image url."
    #     if self.photo:
    #         return '%s%s' % (settings.HOST, self.photo.url)
    #     return ''

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.department_uz:
            self.department_sr = generate_field(self.department_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        # if self.place_uz:
        #     self.place_sr = generate_field(self.place_uz)

        super(Job, self).save(*args, **kwargs)


class StudentActivityCategory(models.Model):
    title = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_activity_category"

    def __str__(self):
        return str(self.title)


    def save(self, *args, **kwargs):
        self.slug = generate_unique_slug(StudentActivityCategory, self.title)

        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(StudentActivityCategory, self).save(*args, **kwargs)

class StudentActivities(models.Model):
    title = models.CharField(max_length=200, null=True)
    content = RichTextField(blank=True, null=True, editable=False)
    category = models.ForeignKey(StudentActivityCategory, on_delete=models.CASCADE, related_name="activities")
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=200, editable=False, blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    short_description = models.CharField(max_length=200, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "student_activities"
        ordering = ["-date"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(StudentActivities, self.title)

        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(StudentActivities, self).save(*args, **kwargs)


class StudentActivityImage(models.Model):
    student_activity = models.ForeignKey(StudentActivities, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="student_activity")




class StudentActivityContent(models.Model):
    student_activity = models.ForeignKey(StudentActivities, on_delete=models.CASCADE, related_name="contents")
    title = models.CharField(max_length=128, null=True)
    content = RichTextField()


class StudentActivityContentTag(models.Model):
    content = models.ForeignKey(StudentActivityContent, on_delete=models.CASCADE, related_name="tags")
    tag = models.CharField(max_length=128, null=True)


class AcademicCalendar(models.Model):
    title = models.CharField(max_length=200, null=True)

class AcademicCalendarFile(models.Model):
    academic_calendar = models.ForeignKey(AcademicCalendar, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="academic_calendar")

from django.core.exceptions import ValidationError

class StudentVideo(models.Model):
    title = models.CharField(max_length=200, null=True)
    video = models.FileField(upload_to="student_video", blank=True, null=True)
    video_url = models.URLField(null=True, blank=True)
    thumbnail = models.ImageField(upload_to="student_video", blank=True, null=True)

    created_at = models.DateTimeField()

    def clean(self):
        if not self.video_url and not self.video:
            raise ValidationError("Video or video url is required")
