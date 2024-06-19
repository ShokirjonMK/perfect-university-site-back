import re

from django.conf import settings
from django.core.validators import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_resized import ResizedImageField
from image_optimizer.fields import OptimizedImageField

from admin_panel.common import generate_field
from hr.utils import generate_unique_slug
from ckeditor.fields import RichTextField

# Image cropping conf
THUMBNAIL = [280, 372]
NEWS_THUMBNAIL = [1280, 720]
VIDEO_GALLERY_THUMBNAIL = [279, 148]
IMAGE = [1200, 675]

# FAQ type
TYPES = (
    (1, _("Huquqiy")),
    (2, _("Psixologik")),
    (3, _("O'smirlar")),
    (4, _("Ayollar")),
)


class NewsProxy(models.Model):
    title = models.CharField(max_length=500)
    description = RichTextField()
    # thumbnail = ResizedImageField(size=NEWS_THUMBNAIL, upload_to='news', blank=True)
    thumbnail = OptimizedImageField(
        upload_to="news",
        optimized_image_output_size=NEWS_THUMBNAIL,
        optimized_image_resize_method="thumbnail",
        blank=True,
    )
    image = ResizedImageField(size=IMAGE, upload_to="news")
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=255, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return "http://api.tpu.uz%s" % self.thumbnail
        
    @property
    def image_url(self):
        if self.image:
            return "http://api.tpu.uz%s" % self.image
            # return "%s%s" % (settings.HOST, self.image.url) if self.image else ""


class NewsHashtagProxy(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.title)


class NewsCategoryProxy(models.Model):
    title = models.CharField(max_length=500)
    slug = models.SlugField(unique=True, max_length=200, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Objective(models.Model):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=500)
    description = RichTextField()
    slug = models.SlugField(unique=True, max_length=200, null=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    icon = models.FileField(upload_to="objective_icons", null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _make_slug(self, value):
        if value is not None:
            original_slug = slugify(value)
            unique_slug = original_slug
            num = 1
            while self.__class__.objects.exclude(pk=self.pk).filter(slug=unique_slug).exists():
                unique_slug = f"{original_slug}-{num}"
                num += 1
            return slugify(unique_slug)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._make_slug(self.title or f"objective-{self.number}")
        return super().save(*args, **kwargs)

    class Meta:
        db_table = "objective"
        ordering = ["number"]
        verbose_name = _("Objective")
        verbose_name_plural = _("Objectives")


class News(NewsProxy):
    short_description = RichTextField()
    category = models.ForeignKey("NewsCategory", on_delete=models.CASCADE, related_name="news")
    hashtag = models.ManyToManyField("NewsHashtag", related_name="news", blank=True)
    objectives = models.ManyToManyField("Objective", related_name="news", blank=True)
    main_page = models.BooleanField(default=False)

    class Meta:
        db_table = "news"
        ordering = ["-publish_date"]

    def save(self, *args, **kwargs):
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.short_description_uz:
            self.short_description_sr = generate_field(self.short_description_uz)
        # slugify
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(News, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(News, self.title_sr)
        if not self.thumbnail:
            self.thumbnail = self.image
        super(News, self).save(*args, **kwargs)



class Gallery(models.Model):
    news = models.ForeignKey("News", on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="news_gallery/")

    @property
    def image_url(self):
        if self.image:
            return "http://api.tpu.uz%s" % self.image
            # return "%s%s" % (settings.HOST, self.image.url) if self.image else ""

    class Meta:
        db_table = "gallery"


class NewsHashtag(NewsHashtagProxy):
    class Meta:
        db_table = "news_hashtags"
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(NewsHashtag, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(NewsHashtag, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(NewsHashtag, self).save(*args, **kwargs)


class NewsCategory(NewsCategoryProxy):
    order = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = "news_categories"
        ordering = ("order",)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(NewsCategory, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(NewsCategory, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(NewsCategory, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class PhotoGallery(models.Model):
    title = models.CharField(max_length=500)
    thumbnail = ResizedImageField(size=THUMBNAIL, upload_to="photo_gallery_thumbnails")
    is_published = models.BooleanField(default=False)
    # main_page = models.BooleanField(default=False)
    # views = models.IntegerField(default=0)

    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "photo_gallery"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def thumbnail_url(self):
        if self.thumbnail:
            return "http://api.tpu.uz%s" % self.thumbnail
        # return "%s%s" % (settings.HOST, self.thumbnail.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(PhotoGallery, self).save(*args, **kwargs)


class PhotoGalleryImage(models.Model):
    photo_gallery = models.ForeignKey(PhotoGallery, on_delete=models.CASCADE, related_name="images")
    image = ResizedImageField(size=IMAGE, upload_to="photo_gallery")

    class Meta:
        db_table = "photo_gallery_images"
        ordering = ["-id"]

    def __str__(self):
        return self.image.name

    @property
    def url(self):
        if self.url:
            return "http://api.tpu.uz%s" % self.url
        # return "%s%s" % (settings.HOST, self.image.url)


class VideoGallery(models.Model):
    title = models.CharField(max_length=500)
    description = RichTextField()
    thumbnail = ResizedImageField(size=VIDEO_GALLERY_THUMBNAIL, upload_to="video_gallery_thumbnails")
    video_link = models.URLField()
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    # main_page = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "video_gallery"
        ordering = ["-publish_date"]

    def __str__(self):
        return str(self.title)

    @property
    def thumb(self):
        if self.thumbnail:
            return "http://api.tpu.uz%s" % self.thumbnail

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)

        super(VideoGallery, self).save(*args, **kwargs)


class Vebinar(models.Model):
    author = models.CharField(max_length=255)
    title = models.CharField(max_length=500)
    thumbnail = ResizedImageField(size=THUMBNAIL, upload_to="video_gallery_thumbnails")
    video_link = models.URLField()
    is_published = models.BooleanField(default=False)
    main_page = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "vebinar"
        ordering = ["-publish_date"]

    def __str__(self):
        return str(self.title)

    @property
    def thumb(self):
        if self.thumbnail:
            return "http://api.tpu.uz%s" % self.thumbnail
        # return "%s%s" % (settings.HOST, self.thumbnail.url)

    def clean(self):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be){1}\/(?:watch\?v=)?(.+)"
        if not re.match(regex, str(self.video_link)):
            raise ValidationError(f"InValid youtube url  {self.video_link}")

    def save(self, *args, **kwargs):
        regex = r"(?:https:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be){1}\/(?:watch\?v=)?(.+)"
        if "embed" not in self.video_link:
            self.video_link = re.sub(regex, r"https://www.youtube.com/embed/\1", self.video_link)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.author_uz:
            self.author_sr = generate_field(self.author_uz)
        super(Vebinar, self).save(*args, **kwargs)


class FAQ(models.Model):
    title = models.CharField(max_length=500)
    author = RichTextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "faq"
        ordering = ["-id"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.author_uz:
            self.author_sr = generate_field(self.author_uz)
        super(FAQ, self).save(*args, **kwargs)

# class Elonlar(models.Model):
#     title = models.CharField(max_length=500)
#     description = models.TextField(null=True, blank=True)
#     # short_description = models.TextField(null=True, blank=True)
#     thumbnail = ResizedImageField(size=THUMBNAIL, upload_to='news')
#     cover = ResizedImageField(upload_to='news')
#     image = ResizedImageField(size=IMAGE, upload_to='news')
#     video_link = models.URLField(null=True, blank=True)
#     views = models.IntegerField(default=0)
#     # category = models.ForeignKey('NewsCategory', on_delete=models.CASCADE, related_name='news')
#     # hashtag = models.ManyToManyField('NewsHashtag', related_name='news', blank=True)
#     main_page = models.BooleanField(default=False)
#     is_published = models.BooleanField(default=False)
#     publish_date = models.DateTimeField(default=timezone.now)
#     updated_at = models.DateTimeField(auto_now=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         db_table = 'newselonlar'
#         ordering = ['-publish_date']
#
#     def __str__(self):
#         return str(self.title)
#
#     @property
#     def thumbnail_url(self):
#         # "Returns the image url."
#         return '%s%s' % (
#             settings.HOST, self.thumbnail.url) if self.thumbnail else ''
#
#     @property
#     def cover_url(self):
#         # "Returns the image url."
#         return '%s%s' % (settings.HOST, self.cover.url) if self.cover else ''
#
#     @property
#     def image_url(self):
#         # "Returns the image url."
#         return '%s%s' % (settings.HOST, self.image.url) if self.image else ''
#
#     def save(self, *args, **kwargs):
#         if self.title_uz:
#             self.title_sr = generate_field(self.title_uz)
#         if self.description_uz:
#             self.description_sr = generate_field(self.description_uz)
#         # if self.short_description_uz:
#         #     self.short_description_sr = generate_field(self.short_description_uz)
#         super(Elonlar, self).save(*args, **kwargs)
