from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.text import slugify
from django_resized import ResizedImageField
from admin_panel.common import generate_field
from django.conf import settings
from ckeditor.fields import RichTextField
import os

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]


def generate_unique_slug(klass, field):
    """
    return unique slug if origin slug is exist.
    eg: `foo-bar` => `foo-bar-1`

    :param `klass` is Class model.
    :param `field` is specific field for title.
    """
    origin_slug = slugify(field)
    unique_slug = origin_slug
    if not origin_slug:
        origin_slug = slugify(generate_field(field))
    numb = 1
    while klass.objects.filter(slug=unique_slug).exists():
        unique_slug = '%s-%d' % (origin_slug, numb)
        numb += 1
    return unique_slug


class StaticPage(models.Model):
    title = models.CharField(max_length=500)
    url = models.CharField(max_length=500, null=True)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    content = RichTextField()
    views = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    image = ResizedImageField(size=IMAGE, upload_to='static_gallery',
                              null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'static_pages'
        ordering = ['-id']

    @property
    def image_name(self):
        # "Returns the image url."
        if self.image:
            return os.path.basename(self.image.name)
        return None

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "http://api.tpu.uz%s" % self.image.url
            # return '%s%s' % (settings.HOST, self.image.url)
        return None

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.url) != self.slug:
                self.slug = generate_unique_slug(StaticPage, self.url)
        else:  # create
            self.slug = generate_unique_slug(StaticPage, self.url)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(StaticPage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class StaticPageImage(models.Model):
    photo_gallery = models.ForeignKey(
        StaticPage, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(size=IMAGE, upload_to='static_gallery')

    class Meta:
        db_table = 'static_page_images'
        ordering = ['-id']

    def __str__(self):
        return self.image.name

    @property
    def image_name(self):
        # "Returns the image url."
        if self.image:
            return os.path.basename(self.image.name)
        return None

    @property
    def url(self):
        # "Returns the image url."
        return "http://api.tpu.uz%s" % self.image.url
        # return '%s%s' % (settings.HOST, self.image.url)


class StudentStaticPages(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    content = RichTextField()
    views = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(StudentStaticPages, self.title)
        else:  # create
            self.slug = generate_unique_slug(StudentStaticPages, self.title)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(StudentStaticPages, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class StudentStaticPagesImage(models.Model):
    photo_gallery = models.ForeignKey(
        StudentStaticPages, on_delete=models.CASCADE, related_name='images')
    image = ResizedImageField(size=IMAGE, upload_to='static_gallery')

    def __str__(self):
        return self.image.name

    @property
    def image_name(self):
        # "Returns the image url."
        if self.image:
            return os.path.basename(self.image.name)
        return None

    @property
    def url(self):
        # "Returns the image url."
        return "http://api.tpu.uz%s" % self.image.url
        # return '%s%s' % (settings.HOST, self.image.url)

class OurMission(models.Model):
    title = models.CharField(verbose_name="Title", max_length=255, null=True)
    description = RichTextField(verbose_name="Description", null=True)
    image = ResizedImageField(size=IMAGE, upload_to='our_mission', null=True, blank=True)
    is_main = models.BooleanField(verbose_name="Is Main", default=False)

    class Meta:
        verbose_name = "Our Mission"
        verbose_name_plural = "Our Missions"


class OurMissionItem(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", null=True)
    our_mission = models.ForeignKey(OurMission, on_delete=models.CASCADE, related_name='mission_item', null=True,
                                    blank=True)

    class Meta:
        verbose_name = "Our Mission Item"
        verbose_name_plural = "Our Mission Items"


class History(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", null=True)
    description = RichTextField(verbose_name="Description", null=True)
    order = models.IntegerField(verbose_name="Order", null=True)

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "History"


class HistoryImage(models.Model):
    image = ResizedImageField(size=IMAGE, upload_to='history', null=True, blank=True)
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name='history_image', null=True,
                                blank=True)

    class Meta:
        verbose_name = "History Image"
        verbose_name_plural = "History Images"


class HistoryYear(models.Model):
    year = models.CharField(max_length=255, verbose_name="Year", null=True)
    title = models.CharField(max_length=255, verbose_name="Title", null=True)
    description = RichTextField(verbose_name="Description", null=True)
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name='history_year', null=True,
                                blank=True)

    class Meta:
        verbose_name = "History Year"
        verbose_name_plural = "History Years"


class HistoryItem(models.Model):
    content = RichTextField(verbose_name="Description", null=True)
    history = models.ForeignKey(History, on_delete=models.CASCADE, related_name='history_item', null=True,
                                blank=True)

    class Meta:
        verbose_name = "History Item"
        verbose_name_plural = "History Items"
