from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _, gettext
from admin_panel.common import generate_field
from admin_panel.model.press_service import NewsProxy, NewsCategoryProxy, NewsHashtagProxy
import os

from ckeditor.fields import RichTextField

from hr.utils import generate_unique_slug

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]


class MonoArticle(models.Model):
    title = models.CharField(max_length=255)

    slug = models.SlugField(max_length=255)
    is_published = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mono_article"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_uz) != self.slug:
                self.slug = generate_unique_slug(MonoArticle, self.title_uz)
        else:  # create
            self.slug = generate_unique_slug(MonoArticle, self.title_uz)

        super(MonoArticle, self).save(*args, **kwargs)


class Section(models.Model):
    section_number = models.PositiveSmallIntegerField(default=1)
    article = models.ForeignKey(MonoArticle, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    order = models.SmallIntegerField(default=1)
    file = models.FileField(upload_to="section_file")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mono_article_section"
        ordering = ["section_number", "order", "id"]

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(Section, self).save(*args, **kwargs)


class MonoFiles(models.Model):
    article = models.ForeignKey(MonoArticle, on_delete=models.CASCADE, related_name="mono_files")
    title = models.CharField(max_length=255)
    # author = models.CharField(max_length=255)
    order = models.SmallIntegerField(default=1)
    file = models.FileField(upload_to="section_file")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "mono_article_files"
        ordering = ["order", "id"]

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(MonoFiles, self).save(*args, **kwargs)


class Conference(models.Model):
    title = models.CharField(max_length=255)
    # order = models.SmallIntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conference"
        ordering = ["-id"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(Conference, self).save(*args, **kwargs)


class ConferenceSubject(models.Model):
    conference = models.ForeignKey(Conference, on_delete=models.CASCADE, related_name="subjects")
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    file = models.FileField(upload_to="conference_file")
    place = models.CharField(max_length=255)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conference_subject"
        ordering = ["-start_date", "id", "conference__id", "conference__pk"]

    @property
    def date(self):
        if self.end_date:
            return (
                f"{self.start_date.day}-{self.end_date.day} {gettext(self.end_date.strftime('%B'))}, "
                f"{self.start_date.year}"
            )
        return f"{self.start_date.day} {gettext(self.start_date.strftime('%B'))}, {self.start_date.year}"

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.department_uz:
            self.department_sr = generate_field(self.department_uz)
        if self.place_uz:
            self.place_sr = generate_field(self.place_uz)
        super(ConferenceSubject, self).save(*args, **kwargs)


class ConferenceTags(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = "conference_tags"
        ordering = ["-id"]
        verbose_name = _("Conference Tag")
        verbose_name_plural = _("Conference Tags")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name_uz:
            self.name_sr = generate_field(self.name_uz)
        super(ConferenceTags, self).save(*args, **kwargs)


class PendingConference(models.Model):
    class ConferenceStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        FINISHED = "finished", _("Finished")

    title = models.CharField(max_length=255, verbose_name=_("Title"))
    icon = models.ImageField(upload_to="conference", verbose_name=_("Icon"), null=True, blank=True)
    slug = models.SlugField(max_length=255, verbose_name=_("Slug"), null=True)
    date = models.DateField(verbose_name=_("Date"))
    start_time = models.TimeField(verbose_name=_("Start Time"), null=True)
    end_time = models.TimeField(verbose_name=_("End Time"), null=True)
    tags = models.ManyToManyField(ConferenceTags, verbose_name=_("Tags"))
    description = RichTextField(verbose_name=_("Description"))
    image = models.ImageField(upload_to="conference", verbose_name=_("Image"))
    views = models.IntegerField(default=0, verbose_name=_("Views"))
    status = models.CharField(max_length=20, choices=ConferenceStatus.choices, default=ConferenceStatus.PENDING)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pending_conference"
        ordering = ["-id"]
        verbose_name = _("Pending Conference")
        verbose_name_plural = _("Pending Conferences")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        super(PendingConference, self).save(*args, **kwargs)


class ConferenceApplication(models.Model):
    class ApplicationStatus(models.TextChoices):
        PENDING = "pending", _("Pending")
        ACCEPTED = "accepted", _("Accepted")
        REJECTED = "rejected", _("Rejected")

    full_name = models.CharField(max_length=255, verbose_name=_("Full Name"))
    phone_number = models.CharField(max_length=255, verbose_name=_("Phone Number"))
    addition_phone_number = models.CharField(max_length=255, verbose_name=_("Addition Phone Number"), blank=True)
    email = models.EmailField(verbose_name=_("Email"), blank=True, null=True)
    file = models.FileField(upload_to="conference_application", verbose_name=_("File"))
    conference = models.ForeignKey(PendingConference, on_delete=models.CASCADE, verbose_name=_("Conference"))
    status = models.CharField(max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "conference_application"
        ordering = ["-id"]
        verbose_name = _("Conference Application")
        verbose_name_plural = _("Conference Applications")

    def __str__(self):
        return self.full_name


class ScienceFiles(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="science-files")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "science-files"
        ordering = [
            "-created_at",
        ]

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None

    @property
    def file_name(self):
        if self.file:
            return os.path.basename(self.file.name)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ScienceFiles, self).save(*args, **kwargs)


class ScienceNewsHashtag(NewsHashtagProxy):
    class Meta:
        db_table = "science_news_hashtags"

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(ScienceNewsHashtag, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(ScienceNewsHashtag, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ScienceNewsHashtag, self).save(*args, **kwargs)


class ScienceNewsCategory(NewsCategoryProxy):
    class Meta:
        db_table = "science_news_categories"

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(ScienceNewsCategory, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(ScienceNewsCategory, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ScienceNewsCategory, self).save(*args, **kwargs)


class ScienceNews(NewsProxy):
    category = models.ForeignKey(ScienceNewsCategory, on_delete=models.CASCADE, related_name="news")
    hashtag = models.ManyToManyField(ScienceNewsHashtag, blank=True, related_name="news")

    class Meta:
        db_table = "science_news"
        ordering = ("-publish_date",)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(ScienceNews, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(ScienceNews, self.title_sr)
        if not self.thumbnail:
            self.thumbnail = self.image
        super(ScienceNews, self).save(*args, **kwargs)


class SeminarHashtag(NewsHashtagProxy):
    class Meta:
        db_table = "seminar_hashtags"

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(SeminarHashtag, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(SeminarHashtag, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(SeminarHashtag, self).save(*args, **kwargs)


class SeminarCategory(NewsCategoryProxy):
    class Meta:
        db_table = "seminar_categories"

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(SeminarCategory, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(SeminarCategory, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(SeminarCategory, self).save(*args, **kwargs)


class Seminar(NewsProxy):
    category = models.ForeignKey(SeminarCategory, on_delete=models.CASCADE, related_name="seminars")
    hashtag = models.ManyToManyField(SeminarHashtag, blank=True, related_name="seminars")

    class Meta:
        db_table = "seminars"
        ordering = ("-publish_date",)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(Seminar, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(Seminar, self.title_sr)
        if not self.thumbnail:
            self.thumbnail = self.image
        super(Seminar, self).save(*args, **kwargs)


class ScienceCenter(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    slug = models.SlugField(max_length=255)
    is_published = models.BooleanField(default=False)
    reception_time = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    fax = models.CharField(max_length=15)
    email = models.EmailField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "science_center"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):

        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.reception_time_uz:
            self.reception_time_sr = generate_field(self.reception_time_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_uz) != self.slug:
                self.slug = generate_unique_slug(ScienceCenter, self.title_uz)
        else:  # create
            self.slug = generate_unique_slug(ScienceCenter, self.title_uz)

        super(ScienceCenter, self).save(*args, **kwargs)
