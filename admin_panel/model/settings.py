from django.conf import settings
from django.db import models
import os
from admin_panel.common import generate_field
from django_resized import ResizedImageField
from django.utils.translation import gettext_lazy as _
from admin_panel.common import generate_field
from ckeditor.fields import RichTextField


class MainPageSetting(models.Model):
    logo = models.FileField(upload_to='agency_logo/')
    logo_white = models.FileField(upload_to='agency_logo/')
    instagram = models.URLField(null=True, blank=True)
    telegram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)
    youtube = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    support = models.URLField("Universitetni boshqarishlab-quvvatlash", null=True, blank=True)

    title = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=128, blank=True, null=True)
    address = RichTextField()
    email = models.EmailField()
    # rekvizit
    fax = models.CharField(max_length=255, default="")
    account_number = models.CharField(max_length=255, default="")
    bank = models.CharField(max_length=255, default="")
    mfo = models.CharField(max_length=255, default="")
    shxr = models.CharField(max_length=255, default="")
    inn = models.CharField(max_length=255, default="")
    okonx = models.CharField(max_length=255, default="")
    #
    location = models.URLField(null=True, blank=True, max_length=500)

    footer_content = RichTextField()
    quote = RichTextField()
    quote_author = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    # banner = models.FileField(upload_to='banner', null=True)
    # banner_link = models.CharField(max_length=100, null=True)

    # number1 = models.CharField(max_length=10, blank=True, null=True)
    # number2 = models.CharField(max_length=10, blank=True, null=True)
    # number3 = models.CharField(max_length=10, blank=True, null=True)
    # number4 = models.CharField(max_length=10, blank=True, null=True)
    #
    # title1 = models.CharField(max_length=128, blank=True, null=True)
    # title2 = models.CharField(max_length=128, blank=True, null=True)
    # title3 = models.CharField(max_length=128, blank=True, null=True)
    # title4 = models.CharField(max_length=128, blank=True, null=True)
    #
    # work_schedule_mon_fri = models.CharField(
    #     max_length=50, blank=True, null=True)
    # work_schedule_sun = models.CharField(max_length=50, blank=True, null=True)
    # work_schedule_lunch = models.CharField(
    #     max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'main_page_settings'

    def __str__(self):
        return 'main_page_settings'

    @property
    def poster_url(self):
        if self.poster:
            return '%s%s' % (settings.HOST, self.poster.url)

    @property
    def logo_url(self):
        if self.logo:
            return '%s%s' % (settings.HOST, self.logo.url)

    @property
    def logo_white_url(self):
        if self.logo_white:
            return '%s%s' % (settings.HOST, self.logo_white.url)

    @property
    def banner_url(self):
        if self.banner:
            return '%s%s' % (settings.HOST, self.banner.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)
        if self.footer_content_uz:
            self.footer_content_sr = generate_field(self.footer_content_uz)
        if self.quote_uz:
            self.quote_sr = generate_field(self.quote_uz)
        if self.quote_author_uz:
            self.quote_author_sr = generate_field(self.quote_author_uz)
        super(MainPageSetting, self).save(*args, **kwargs)


class TopLink(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='child')
    title = models.CharField(max_length=255)
    link = models.URLField(null=True, blank=True)
    order = models.SmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'top_link'
        ordering = ('order',)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(TopLink, self).save(*args, **kwargs)


class Slider(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    image = models.FileField(upload_to='slider')
    order = models.SmallIntegerField(default=1)
    link = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slider'
        ordering = ('order',)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        if self.image:
            return '%s%s' % (settings.HOST, self.image.url)

    @property
    def image_name_uz(self):
        if self.image_uz:
            return os.path.basename(self.image_uz.name)
        return None

    @property
    def image_name_ru(self):
        if self.image_ru:
            return os.path.basename(self.image_ru.name)
        return None

    @property
    def image_name_en(self):
        if self.image_en:
            return os.path.basename(self.image_en.name)
        return None

    def save(self, *args, **kwargs):
        if self.short_description_uz:
            self.short_description_sr = generate_field(self.short_description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Slider, self).save(*args, **kwargs)


# Xatolik
class Typo(models.Model):
    title = RichTextField(null=True, blank=True)
    comment = RichTextField(null=True, blank=True)
    corrected = models.BooleanField(default=False)
    page = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'typos'
        ordering = ['corrected']

    def __str__(self):
        return "{} {} {}".format(
            ("Completed" if self.corrected else "Not completed"),
            self.created_at, self.page)


class MediaImage(models.Model):
    image = ResizedImageField(size=[1200, 675], upload_to='uploads')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ""


SIDEBAR_IMAGE = [279, 287]


class Sidebar(models.Model):
    title = models.CharField(max_length=255)
    image = ResizedImageField(SIDEBAR_IMAGE)
    button_title = models.CharField(max_length=64)
    link = models.URLField()
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.button_title_uz:
            self.button_title_sr = generate_field(self.button_title_uz)
        super(Sidebar, self).save(*args, **kwargs)

    @property
    def image_url(self):
        # "Returns the image url."
        return '%s%s' % (settings.HOST, self.image.url) if self.image else ""

    def __str__(self):
        return self.title


class MainPageData(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_("Default Main Page Active"))

    class Meta:
        verbose_name = _("Main Page Data")
        verbose_name_plural = _("Main Page Data")

    def __str__(self):
        return self.title


class FAQQuestion(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.SmallIntegerField(default=1)

    class Meta:
        ordering = (
            "order",
            "-created_at",
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(FAQQuestion, self).save(*args, **kwargs)
