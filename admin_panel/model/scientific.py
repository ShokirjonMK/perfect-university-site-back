from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from admin_panel.common import generate_field
from hr.models import BaseModel

from ckeditor.fields import RichTextField


class ScientificJournal(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("title"))
    description = RichTextField(_("Description"), null=True)
    file = models.FileField(upload_to="scientific-file")
    image = models.ImageField(upload_to="scientific")
    date = models.DateField(null=True)

    def __str__(self):
        return f"{self.title}- ({self.id})"

    class Meta:
        db_table = "scientific_journal"
        verbose_name = _("Scientific Journal")
        verbose_name_plural = _("Scientific Journals")
        ordering = ("created_at",)

    @property
    def image_url(self):
        # "Returns the image url."
        return "http://api.tpu.uz%s" % self.image.url if self.image else ""
        # return "%s%s" % (settings.HOST, self.image.url) if self.image else ""

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return None

    @property
    def get_file(self):
        if self.file:
            return self.file.url
        else:
            return None

    def save(self, *args, **kwargs):
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ScientificJournal, self).save(*args, **kwargs)


class ScientificJournalDesc(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = RichTextField(_("Description"))

    def __str__(self):
        return f"{self.title}- ({self.id})"

    class Meta:
        verbose_name = _("Scientific Journal Desc")
        ordering = ("created_at",)

    def save(self, *args, **kwargs):
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(ScientificJournalDesc, self).save(*args, **kwargs)
