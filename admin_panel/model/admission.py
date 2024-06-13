from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from admin_panel.model import territorial
from phonenumber_field.modelfields import PhoneNumberField

from ckeditor.fields import RichTextField

class PersonalDetailAbstract(models.Model):
    MALE = _("Male")
    FEMALE = _("Female")
    _gender_choices = (
        (1, MALE),
        (2, FEMALE),
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(max_length=255)
    citizenship = models.ForeignKey(
        territorial.Country, on_delete=models.SET_NULL, null=True, blank=True, related_name="citizenship"
    )
    nationality = models.ForeignKey(
        territorial.Nationality,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    passport = models.CharField(max_length=31)
    gender = models.SmallIntegerField(choices=_gender_choices)
    passport_copy = models.FileField(
        upload_to="passports", validators=[FileExtensionValidator(allowed_extensions=["pdf", "png", "jpg", "jpeg"])]
    )
    phone_number = PhoneNumberField(null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.first_name

    @property
    def title(self):
        return f"{self.first_name} {self.last_name}"


class EducationalAbstract(models.Model):
    Q_TOEFL_SCORE = "TOEFL"
    Q_CEFR_SCORE = "CEFR"
    Q_IELTS_SCORE = "IELTS"
    Q_NO_SCORE = "No Score"
    _language_q_choices = (
        (0, Q_TOEFL_SCORE),
        (1, Q_CEFR_SCORE),
        (2, Q_IELTS_SCORE),
        (3, Q_NO_SCORE),
    )
    _certificate_choices = (
        (1, "Certificate"),
        (2, "Academic lyceum diploma"),
        (3, "Secondary specialized and vocational College diploma"),
        (0, "Others"),
    )

    education_name = models.CharField(max_length=500, null=True)
    certificate = models.SmallIntegerField(choices=_certificate_choices, null=True)
    graduation_year = models.DateField(null=True)
    document_series_number = models.CharField(max_length=255, null=True)
    diploma = models.FileField(
        upload_to="diploma",
        verbose_name="Copy of the higher education document",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["doc", "docx", "gif", "jpg", "pdf", "png", "jpeg", "zip"])
        ],
    )
    language_qualifications = models.SmallIntegerField(choices=_language_q_choices, null=True)
    have_higher_education = models.BooleanField(default=False, null=True)
    higher_education_name = models.CharField(max_length=255, null=True, blank=True)
    national_olympiads = RichTextField(blank=True, null=True)
    disability = RichTextField(blank=True, null=True)
    need_dormitory = models.BooleanField(default=False)
    region = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

    class Meta:
        abstract = True
