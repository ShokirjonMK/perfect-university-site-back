from django.db import models
from django.utils.translation import gettext_lazy as _
from admin_panel.model.territorial import Nationality
from admin_panel.common import generate_field
from django.conf import settings

from ckeditor.fields import RichTextField


class FIELD_TYPES(models.IntegerChoices):
    text = 1, _("text")
    email = 2, _("email")
    textarea = 3, _("textarea")
    date = 4, _("date")
    select = 5, _("select")
    file = 6, _("file")
    radio = 7, _("radio")
    checkbox = 8, _("checkbox")
    checkbox_with_textarea = 9, _("checkbox + textarea")
    checkbox_with_file = 10, _("checkbox + file")


class FIELD_STEPS(models.IntegerChoices):
    # step_1 = 1, _("Shaxsiy ma'lumotlar")
    step_2 = 2, _("Ta'lim")
    step_3 = 3, _("Ilmiy")
    step_4 = 4, _("Mahorat")


class ChoiceFieldOptions(models.Model):
    field = models.ForeignKey("VacancyField", on_delete=models.CASCADE, verbose_name="Field", related_name="options")
    title = models.CharField(_("Nomi"), max_length=512)


class VacantFileField(models.Model):
    file = models.FileField(upload_to="vacancy")


class Position(models.Model):
    title = models.CharField(_("Lavozim"), max_length=255)
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(Position, self).save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Lavozim")
        verbose_name_plural = _("Lavozimlar")


class Form(models.Model):
    title = models.CharField(_("Forma nomi"), max_length=512)
    positions = models.ManyToManyField(Position, verbose_name="Lavozimlar")
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Vacancy Forma")
        verbose_name_plural = _("Vacancy Formalar")


class VacancyField(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="fields")
    step = models.SmallIntegerField(verbose_name=_("Step"), choices=FIELD_STEPS.choices)
    title = models.CharField(_("Nomi"), max_length=512, null=True, blank=True)
    field_type = models.SmallIntegerField(_("Field turi"), choices=FIELD_TYPES.choices)
    placeholder = models.CharField(_("Placeholder"), max_length=512, null=True, blank=True)
    required = models.BooleanField(_("Is required?"), default=True)
    toggle = models.BooleanField(_("Is required?"), default=False)

    class Meta:
        ordering = ["step", "id"]
        verbose_name = _("Vacancy field")
        verbose_name_plural = _("Vacancy fields")

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.placeholder_uz:
            self.placeholder_sr = generate_field(self.placeholder_uz)
        super(VacancyField, self).save(*args, **kwargs)


class Vacant(models.Model):
    status = models.IntegerField(
        _("Holati"),
        choices=(
            (1, _("Yangi")),
            (2, _("Ko'rib chiqilgan")),
        ),
        default=1,
    )
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="vacants", verbose_name=_("Forma"))
    MALE = _("Erkak")
    FEMALE = _("Ayol")
    _gender_choices = (
        (1, MALE),
        (2, FEMALE),
    )
    first_name = models.CharField(_("Ismingiz"), max_length=255)
    last_name = models.CharField(_("Familiyangiz"), max_length=255)
    middle_name = models.CharField(_("Sharifingiz"), max_length=255)
    date_of_birth = models.DateField(_("Tug‘ilgan sana"))
    gender = models.SmallIntegerField(_("Jinsingiz"), choices=_gender_choices)
    nationality = models.ForeignKey(
        Nationality, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Millatingiz")
    )
    phone_number = models.CharField(max_length=255, verbose_name=_("Telefon raqamingiz"))
    email = models.EmailField(_("Elektron pochta manzilingiz"))

    address = models.CharField(_("Yashash manzilingiz"), max_length=1024)
    photo = models.OneToOneField(
        VacantFileField, on_delete=models.SET_NULL, null=True, verbose_name=_("Rasmingiz (3x4)")
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE, verbose_name=_("Lavozimingizni tanlang"))
    created_at = models.DateTimeField(_("Yaratilgan vaqt"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan vaqt"), auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ishga arizachi")
        verbose_name_plural = _("Ishga arizachilar")


class VacantFieldValue(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    vacant = models.ForeignKey(Vacant, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Arizachi"))
    step = models.SmallIntegerField(verbose_name=_("Step"), choices=FIELD_STEPS.choices)
    title = models.CharField(_("Nomi"), max_length=512, null=True, blank=True)
    field_type = models.SmallIntegerField(_("Field turi"), choices=FIELD_TYPES.choices)
    value = RichTextField()

    def __str__(self):
        return self.title

    @property
    def get_value(self):
        if self.field_type == 8:
            return f'<a href="{settings.MEDIA_URL}/{self.value}">{self.value}</a>'
        else:
            return self.value

    class Meta:
        ordering = ["step", "id"]
        verbose_name = _("Ma'lumot")
        verbose_name_plural = _("Ma'lumotlar")
