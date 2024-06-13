import os.path

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from admin_panel.common import generate_field
from admin_panel.model.press_service import NewsProxy
from admin_panel.model.courses import CourseCatalog
from hr.utils import generate_unique_slug

from ckeditor.fields import RichTextField

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]


class Grant(NewsProxy):
    short_description = RichTextField()
    thumbnail = None

    # image = None

    class Meta:
        db_table = "grants"
        ordering = ["-publish_date"]

    @property
    def image_name(self):
        # "Returns the image url."
        if self.image:
            return os.path.basename(self.image.name)
        return ""

    def save(self, *args, **kwargs):
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.short_description_uz:
            self.short_description_sr = generate_field(self.short_description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(Grant, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(Grant, self.title_sr)
        if not self.thumbnail:
            self.thumbnail = self.image
        super(Grant, self).save(*args, **kwargs)


class GrantFiles(models.Model):
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="grant-file")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "grant_file"
        ordering = ("created_at",)

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None

    @property
    def file_name(self):
        # "Returns the image url."
        if self.file:
            return os.path.basename(self.file.name).split(".")[0]
        return ""

    @property
    def file_type(self):
        # "Returns the image url."
        if self.file:
            return os.path.basename(self.file.name).split(".")[1]
        return ""

    def __str__(self):
        return str(self.id)


class InternationalConferencePage(models.Model):
    image = ResizedImageField(size=IMAGE, upload_to="international/conferences")
    title = models.CharField(max_length=255, null=True)
    content = RichTextField()
    # conferences = models.ManyToManyField(ConferenceSubject,
    #                                      related_name='international')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "international_conferencepage"
        ordering = ["-updated_at"]

    @property
    def image_url(self):
        # "Returns the image url."
        return "%s%s" % (settings.HOST, self.image.url) if self.image else ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.content_sr = generate_field(self.title_uz)

        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(InternationalConferencePage, self).save(*args, **kwargs)


# Sirtqi bo'lim
class ExternalSection(models.Model):
    image = ResizedImageField(size=IMAGE, upload_to="external_sections")
    title = models.CharField(max_length=255, null=True)
    content = RichTextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "external_section"
        ordering = ["-updated_at"]

    @property
    def image_url(self):
        # "Returns the image url."
        return "%s%s" % (settings.HOST, self.image.url) if self.image else ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.content_sr = generate_field(self.title_uz)

        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(self.__class__, self).save(*args, **kwargs)


# class InternationalConferences(models.Model):
#     page = models.ForeignKey(InternationalConferencePage,on_delete=models.CASCADE,related_name='conferences')
#     title = models.CharField(max_length=255)
#     department = models.CharField(max_length=255)
#     page_link = models.URLField()
#     place = models.CharField(max_length=255)
#     start_date = models.DateField(default=timezone.now)
#     end_date = models.DateField(null=True, blank=True)
#
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'international_conferences'
#         ordering = ['-start_date']
#
#     @property
#     def date(self):
#         if self.end_date:
#             return f"{self.start_date.day}-{self.end_date.day} {gettext(self.end_date.strftime('%B'))},
#             {self.start_date.year}"
#         return f"{self.start_date.day} {gettext(self.start_date.strftime('%B'))}, {self.start_date.year}"
#
#     def __str__(self):
#         return self.title
#
#     def save(self, *args, **kwargs):
#         if self.title_uz:
#             self.title_sr = generate_field(self.title_uz)
#         if self.department_uz:
#             self.department_sr = generate_field(self.department_uz)
#         if self.place_uz:
#             self.place_sr = generate_field(self.place_uz)
#         super(InternationalConferences, self).save(*args, **kwargs)


class InternationalRelation(models.Model):
    title = models.CharField(max_length=500)
    image = models.ImageField(upload_to="internationalrelations")
    short_description = RichTextField()
    link = models.URLField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return self.title

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return None

    def save(self, *args, **kwargs):
        if self.short_description_uz:
            self.short_description_sr = generate_field(self.short_description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(InternationalRelation, self).save(*args, **kwargs)


class InternationalStaff(models.Model):
    title = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    image = models.ImageField(upload_to="international-staff")
    short_description = RichTextField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return None

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return self.title

    def save(self, *args, **kwargs):
        if self.short_description_uz:
            self.short_description_sr = generate_field(self.short_description_uz)
        super(InternationalStaff, self).save(*args, **kwargs)


class InternationalUsufulLink(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class InternationalPartnerPage(models.Model):
    title = models.CharField(max_length=500)
    content = RichTextField()
    views = models.IntegerField(default=0)
    image = ResizedImageField(size=IMAGE, upload_to="static_gallery", null=True)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return self.title

    @property
    def image_url(self):
        if self.image:
            # "Returns the image url."
            return "%s%s" % (settings.HOST, self.image.url)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(InternationalPartnerPage, self).save(*args, **kwargs)


class InternationalPartner(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    image = models.FileField(upload_to="static_gallery")

    def __str__(self):
        return self.title

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return self.title

    @property
    def image_url(self):
        if self.image:
            # "Returns the image url."
            return "%s%s" % (settings.HOST, self.image.url)
        return None


class InternationalFacultyPage(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    content = RichTextField(verbose_name=_("Content"))
    video_url = models.URLField(verbose_name=_("Video URL"))

    def __str__(self):
        return self.title


class InternationalFacultyApplication(models.Model):
    full_name = models.CharField(max_length=255, verbose_name=_("Full name"))
    category = models.ForeignKey(CourseCatalog, on_delete=models.CASCADE, verbose_name=_("Category"))
    passport_front = models.ImageField(upload_to="international_faculty")
    passport_back = models.ImageField(upload_to="international_faculty")
    image_3_4 = models.ImageField(upload_to="international_faculty")

    birth_date = models.DateField(verbose_name=_("Birth date"))
    address = models.CharField(max_length=500, verbose_name=_("Address"))
    phone_number1 = models.CharField(max_length=30, verbose_name=_("Phone number 1"))
    phone_number2 = models.CharField(max_length=30, verbose_name=_("Phone number 2"), null=True, blank=True)
    school_number = models.CharField(verbose_name=_("School number"), max_length=200)

    is_reviewed = models.BooleanField(default=False, verbose_name=_("Is reviewed"))
    is_form_invalid = models.BooleanField(default=False, verbose_name=_("Is form invalid"))

    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.id}. {self.full_name} - {self.phone_number1}"


class InternationalCooperationCategory(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    slug = models.SlugField(max_length=500, verbose_name=_("Slug"), unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self.__class__, self.title)
        super(InternationalCooperationCategory, self).save(*args, **kwargs)


class InternationalCooperation(models.Model):
    title = models.CharField(max_length=500, verbose_name=_("Title"))
    content = RichTextField(verbose_name=_("Content"))
    image = ResizedImageField(upload_to="international_cooperation", null=True, blank=True)
    link = models.URLField(verbose_name=_("Link"), null=True, blank=True)
    category = models.ForeignKey(InternationalCooperationCategory, on_delete=models.CASCADE, verbose_name=_("Category"))

    def __str__(self):
        return self.title

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return self.title

    @property
    def image_url(self):
        if self.image:
            # "Returns the image url."
            return "%s%s" % (settings.HOST, self.image.url)
        return None

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        super(InternationalCooperation, self).save(*args, **kwargs)


class Ranking(models.Model):
    image = models.ImageField(upload_to="ranking")
    reputation_ranking = models.FloatField(verbose_name=_("Reputation ranking"))
    academic_reputation_ranking = models.FloatField(verbose_name=_("Academic reputation ranking"))
    employer_reputation_ranking = models.FloatField(verbose_name=_("Employer reputation ranking"))
    reputation_assessment = models.FloatField(verbose_name=_("Reputation assestment"))

    class Meta:
        verbose_name = _("Ranking")
        verbose_name_plural = _("Rankings")


class JointPrograms(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    image = models.ImageField(upload_to="joint_programs", verbose_name=_("Image"))
    link = models.URLField(verbose_name=_("Link"))
    order = models.IntegerField(verbose_name=_("Order"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Joint program")
        verbose_name_plural = _("Joint programs")
        ordering = ["order"]
