from django.conf import settings
from django.db import models
from django.utils import timezone
from admin_panel.common import generate_field
from django.utils.translation import gettext_lazy as _, gettext


class Docs(models.Model):
    law = models.CharField(max_length=500)
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="docs")
    date = models.DateTimeField(default=timezone.now)
    number = models.CharField(max_length=64)

    is_published = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "docs"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return str(self.law)

    @property
    def law_date(self):
        return f"{self.date.year} {_('yil')} {self.date.day} {gettext(self.date.strftime('%B'))} № {self.number}"

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.law_uz:
            self.law_sr = generate_field(self.law_uz)

        super(Docs, self).save(*args, **kwargs)


class Report(models.Model):
    quarter1 = _("1-chorak")
    quarter2 = _("2-chorak")
    quarter3 = _("3-chorak")
    quarter4 = _("4-chorak")
    yearly = _("yillik")
    half_year = _("yarim yillik")
    nine_monthly = _("9 oylik")

    _quarter_choices = (
        (1, quarter1),
        (2, quarter2),
        (3, quarter3),
        (4, quarter4),
        (5, yearly),
        (6, half_year),
        (7, nine_monthly),
    )

    title = models.CharField(max_length=500)
    date = models.DateTimeField(default=timezone.now)
    quarter = models.SmallIntegerField(choices=_quarter_choices, default=1)
    file = models.FileField(upload_to="reports")

    is_published = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reports"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)

        super(Report, self).save(*args, **kwargs)


class LawyerPage(models.Model):
    title = models.CharField(max_length=500)
    file = models.FileField(upload_to="lawyer-page")
    date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lawyer_page"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return self.title

    @property
    def file_url(self):
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(LawyerPage, self).save(*args, **kwargs)
