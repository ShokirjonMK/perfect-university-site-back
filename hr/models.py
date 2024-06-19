from django.db import models
from django.utils.translation import gettext_lazy as _
from .utils import generate_field
from django.utils import timezone
from django.conf import settings


class BaseModel(models.Model):
    created_at = models.DateTimeField(_("Kiritilgan sana"), auto_now_add=True)
    updated_at = models.DateTimeField(_("O'zgartirilgan sana"), auto_now=True)

    class Meta:
        abstract = True


class Nationality(BaseModel):
    title = models.CharField(max_length=255)

    class Meta:
        ordering = ["-title"]

    def __str__(self):
        return str(self.title)


class FIELD_TYPES(models.IntegerChoices):
    text = 1, _("text")  # default: options:[]
    email = 2, _("email")  # default: options:[]
    textarea = 3, _("textarea")  # default: options:[]
    date = 4, _("date")  # default: options:[], placeholder: ''
    select = 5, _("select")
    file = 6, _("file")  # default: options:[]
    radio = 7, _("radio")
    checkbox = 8, _("checkbox")  # default: placeholder:""
    checkbox_with_textarea = 9, _("checkbox + textarea")
    checkbox_with_file = 10, _("checkbox + file")
    work_experience = 11, _("Ish tajribasi")


class FIELD_STEPS(models.IntegerChoices):
    # step_1 = 1, _("Shaxsiy ma'lumotlar")
    step_2 = 2, _("Ta'lim")
    step_3 = 3, _("Ilmiy")
    step_4 = 4, _("Mahorat")
    step_5 = 5, _("Mehnat faoliyati")


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


class Form(BaseModel):
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


class Vacant(BaseModel):
    status = models.IntegerField(
        _("Holati"),
        choices=(
            (1, _("Yangi")),
            (2, _("Ko'rib chiqilgan")),
        ),
        default=1,
    )
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="vacants", verbose_name=_("Forma"))
    vacancy = models.ForeignKey("Job", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Vakansiya"))
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
    passport_file = models.OneToOneField(
        VacantFileField,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Pasportingiz"),
        related_name="passport_file",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ishga arizachi")
        verbose_name_plural = _("Ishga arizachilar")


class VacantFieldValue(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    vacant = models.ForeignKey(Vacant, on_delete=models.CASCADE, related_name="fields", verbose_name=_("Arizachi"))
    step = models.SmallIntegerField(verbose_name=_("Step"), choices=FIELD_STEPS.choices)
    title = models.CharField(_("Nomi"), max_length=512, null=True, blank=True)
    from_date = models.DateField(_("Boshlang‘ich sanasi"), null=True, blank=True)
    from_to = models.DateField(_("Tugash sanasi"), null=True, blank=True)
    field_type = models.SmallIntegerField(_("Field turi"), choices=FIELD_TYPES.choices)
    value = models.TextField()

    def __str__(self):
        return self.title

    @property
    def get_value(self):
        if self.field_type == 6:
            return f'<a href="{settings.HOST}/{self.value}">Yuklab olish</a>'
        return self.value

    class Meta:
        ordering = ["step", "id"]
        verbose_name = _("Ma'lumot")
        verbose_name_plural = _("Ma'lumotlar")


class JobCategory(BaseModel):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if self.name_uz:
            self.name_sr = generate_field(self.name_uz)
        super(JobCategory, self).save(*args, **kwargs)


class Job(BaseModel):
    title = models.CharField(max_length=200, null=True)
    department = models.CharField(max_length=200)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    form = models.ForeignKey(Form, on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.BigIntegerField(default=0)
    salary_to = models.BigIntegerField(null=True, blank=True)
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.department_uz:
            self.department_sr = generate_field(self.department_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Job, self).save(*args, **kwargs)


class MediaImage(models.Model):
    image = models.ImageField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)

    @property
    def image_url(self):
        # "Returns the image url."
        return "http://api.tpu.uz%s" % self.image.url if self.image else ""
        return "%s%s" % (settings.HOST, self.image.url) if self.image else ""


class NewVacant(BaseModel):
    status = models.IntegerField(
        _("Holati"),
        choices=(
            (1, _("Yangi")),
            (2, _("Ko'rib chiqilgan")),
        ),
        default=1,
    )
    phone_number = models.CharField(max_length=255, verbose_name=_("Telefon raqamingiz"))
    vacancy = models.ForeignKey("Job", on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Vakansiya"))
    resume_file = models.FileField(upload_to="vacancy", verbose_name=_("Rezyume"), null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Ishga arizachi")
        verbose_name_plural = _("Ishga arizachilar")

    def __str__(self):
        return str(self.phone_number)

# @receiver(post_save, sender=Nationality)
# def update_stock(sender, instance, created, **kwargs):
#     data = NationalityTransferSerializer(instance).data
#     if created:
#         requests.post(f"{settings.TRANSFER_HOST}/hr/transfer/nationality-create/", json=data)
#     else:
#         requests.put(f"{settings.TRANSFER_HOST}/hr/transfer/nationality-update/{instance.pk}/", json=data)
#
#
# @receiver(post_delete, sender=Nationality)
# def update_stockpost_delete(sender, instance, **kwargs):
#     requests.delete(f"{settings.TRANSFER_HOST}/hr/transfer/nationality-delete/{instance.pk}/")


