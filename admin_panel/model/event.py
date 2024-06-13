from django.db import models
from django.utils import timezone

from admin_panel.common import generate_field
from django.utils.text import Truncator, slugify
from django.utils.html import strip_tags
from config.helpers import generate_unique_slug
from django.utils.translation import gettext_lazy as _g

from ckeditor.fields import RichTextField

# Image cropping conf
THUMBNAIL = [300, 170]
IMAGE = [1200, 675]


class EventsHashtag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "events_hashtags"
        ordering = ("-updated_at",)

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(EventsHashtag, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(EventsHashtag, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(EventsHashtag, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)


class Event(models.Model):
    NOW = _g("Davom etmoqda")
    WAIT = _g("Kutilayotgan")
    END = _g("Yakunlangan")
    title = models.CharField(max_length=255)
    description = RichTextField()
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(default=timezone.now)
    # address = models.TextField()
    # event_place = models.TextField()
    # link = models.URLField(null=True)
    # image = ResizedImageField(size=IMAGE, upload_to='event')
    # event_date = models.DateTimeField(default=timezone.now)
    main_page = models.BooleanField(default=False)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, related_name='event')
    # pin = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    hashtag = models.ManyToManyField(EventsHashtag, blank=True, related_name="events")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def event_date(self):
        return self.start_time

    class Meta:
        db_table = "events"
        ordering = ["-start_time"]

    def __str__(self):
        return str(self.title)

    @property
    def short_description(self):
        return Truncator(strip_tags(self.description)).words(18, html=False)

    @property
    def duration(self):
        if self.start_time.date() == self.end_time.date():
            return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
        else:
            return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M %d.%m.%y')}"

    @property
    def status(self):
        now = timezone.now()
        if now.date() == self.start_time.date():
            if self.start_time.time() < now.time() and self.end_time.time() > now.time():
                return self.NOW
            elif self.start_time.time() < now.time():
                return self.END
            else:
                return self.WAIT
        elif self.start_time.date() < now.date():
            return self.END
        else:
            return self.WAIT

    # @property
    # def image_url(self):
    #     # "Returns the image url."
    #     return '%s%s' % (settings.HOST, self.image.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        # if self.address_uz:
        #     self.address_sr = generate_field(self.address_uz)
        # if self.event_place_uz:
        #     self.event_place_sr = generate_field(self.event_place_uz)

        super(Event, self).save(*args, **kwargs)
