from django.db import models

from admin_panel.common import generate_field
from config import settings

from ckeditor.fields import RichTextField

class Service(models.Model):
    title = models.CharField(max_length=500, null=True, blank=False)
    icon = models.FileField(upload_to="icon", null=True, blank=True)
    main_icon = models.FileField(upload_to="icon", null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    content = RichTextField(null=True, blank=True)
    order = models.IntegerField(null=True, blank=True)
    main_page = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "service"
        ordering = ["order", "created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def icon_url(self):
        if self.icon:
            # "Returns the image url."
            return "http://api.tpu.uz%s" % self.icon.url
            # return "%s%s" % (settings.HOST, self.icon.url)

    @property
    def white_icon_url(self):
        # "Returns the image url."
        if self.main_icon:
            return "http://api.tpu.uz%s" % self.main_icon.url
            # return "%s%s" % (settings.HOST, self.main_icon.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        super(Service, self).save(*args, **kwargs)
