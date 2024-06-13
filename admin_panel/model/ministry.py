from django.conf import settings
from django.db import models
from django.utils import timezone
import os
from django_resized import ResizedImageField
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
# Image cropping conf
from django.utils.text import slugify
from admin_panel.common import generate_field
from admin_panel.model.territorial import Region
from hr.utils import generate_unique_slug
from ckeditor.fields import RichTextField

THUMBNAIL = [300, 170]
IMAGE = [800, 800]
STAFF_IMAGE = [279, 250]


class Statistic(models.Model):
    title = models.CharField(max_length=255)
    icon = models.FileField(null=True, upload_to="statistic", verbose_name="White Icon",
                            validators=[FileExtensionValidator(allowed_extensions=['svg'])])
    blue_icon = models.FileField(null=True, upload_to="statistic", verbose_name="Blue icon",
                                 validators=[FileExtensionValidator(allowed_extensions=['svg'])])
    content = RichTextField()
    why_tsue = RichTextField(null=True)
    image = models.FileField(upload_to="statistic", null=True)
    link = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "statistic"

    def __str__(self):
        return self.title

    @property
    def icon_url(self):
        if self.icon:
            return "%s%s" % (settings.HOST, self.icon.url)

    @property
    def blue_icon_url(self):
        if self.blue_icon:
            return "%s%s" % (settings.HOST, self.blue_icon.url)

    @property
    def image_url(self):
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)

    @property
    def icon_name(self):
        if self.icon:
            return os.path.basename(self.icon.name)
        return None

    @property
    def image_name(self):
        if self.icon:
            return os.path.basename(self.image.name)
        return None

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Statistic, self).save(*args, **kwargs)


class StatisticItem(models.Model):
    order = models.SmallIntegerField(default=1)
    title = models.CharField(max_length=255)
    number = models.IntegerField()
    image = models.FileField(upload_to="statistic")
    blue_image = models.FileField(upload_to="statistic", null=True)

    class Meta:
        db_table = "statistic_item"
        ordering = ("order",)

    def __str__(self):
        return self.title

    @property
    def icon_url(self):
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)

    @property
    def blue_icon_url(self):
        if self.blue_image:
            return "%s%s" % (settings.HOST, self.blue_image.url)

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return None

    @property
    def blue_image_name(self):
        if self.blue_image:
            return os.path.basename(self.blue_image.name)
        return None

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        super(StatisticItem, self).save(*args, **kwargs)


class StatisticContentItem(models.Model):
    content = RichTextField()
    order = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "Statistic Content Item"
        verbose_name_plural = "Statistic Content Items"
        db_table = "statistic_content_item"
        ordering = ("order",)


class ForeignStudent(models.Model):
    background_image = ResizedImageField(size=IMAGE, upload_to="foreign_student")
    youtube_link = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.youtube_link

    @property
    def background_image_name(self):
        if self.background_image:
            return os.path.basename(self.background_image.name)
        return None

    class Meta:
        verbose_name = "Foreign Student"
        verbose_name_plural = "Foreign Students"
        db_table = "foreign_student"



class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    link = models.URLField()

    class Meta:
        db_table = "announcement"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Announcement, self).save(*args, **kwargs)


class FamousGraduate(models.Model):
    title = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    faculty = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    image = models.ImageField(upload_to="famousgraduates")
    quote = RichTextField()
    bio = RichTextField()
    tasks = RichTextField()
    order = models.SmallIntegerField(default=1)
    slug = models.SlugField(max_length=200, unique=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "famousgraduates"
        ordering = ("order",)

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        # "Returns the image url."
        return "%s%s" % (settings.HOST, self.image.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.profession_uz:
            self.profession_sr = generate_field(self.profession_uz)
        if self.faculty_uz:
            self.faculty_sr = generate_field(self.faculty_uz)
        if self.year_uz:
            self.year_sr = generate_field(self.year_uz)
        if self.slug:  # edit
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(FamousGraduate, self.title)
        else:  # create
            self.slug = generate_unique_slug(FamousGraduate, self.title)
        super(FamousGraduate, self).save(*args, **kwargs)


class FamousGraduateGallery(models.Model):
    famousgraduate = models.ForeignKey(FamousGraduate, on_delete=models.CASCADE, related_name="images")
    image = ResizedImageField(size=IMAGE, upload_to="photo_gallery")
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "famous_graduate_gallery"
        ordering = ["-created_at"]

    def __str__(self):
        return self.famousgraduate.title

    @property
    def image_url(self):
        # "Returns the image url."
        return "%s%s" % (settings.HOST, self.image.url)


class AboutMinistry(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    content = RichTextField(null=True)
    image1 = models.ImageField(upload_to="aboutministry/")
    image2 = models.ImageField(upload_to="aboutministry/")
    image3 = models.ImageField(upload_to="aboutministry/")
    file = models.FileField(upload_to="aboutministry/", null=True)

    # views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "about_ministry"

    @property
    def image_urls(self):
        urls = []
        if self.image1:
            urls.append("%s%s" % (settings.HOST, self.image1.url))
        if self.image2:
            urls.append("%s%s" % (settings.HOST, self.image2.url))
        if self.image3:
            urls.append("%s%s" % (settings.HOST, self.image3.url))
        return urls

    @property
    def logo_url(self):
        if self.logo:
            return "%s%s" % (settings.HOST, self.logo.url)

    @property
    def director_logo_url(self):
        if self.director_logo:
            return "%s%s" % (settings.HOST, self.director_logo.url)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(AboutMinistry, self).save(*args, **kwargs)


class Goal(models.Model):
    title = models.CharField(max_length=500, blank=True, null=True)
    content = RichTextField(null=True)
    views = models.IntegerField(default=0)
    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "goal"

    def __str__(self):
        return str(self.content)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Goal, self).save(*args, **kwargs)


class Structure(models.Model):
    title = models.CharField(max_length=500)
    content = RichTextField(null=True)
    views = models.IntegerField(default=0)
    order = models.IntegerField(default=0)
    # publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "structure"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def type(self):
        return "structure"

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Structure, self).save(*args, **kwargs)


# Extra departments for STAFF fakultet
class Department(models.Model):
    title = models.CharField(max_length=255)
    # content = models.TextField(null=True)
    # views = models.IntegerField(default=0)
    image = models.FileField(upload_to="facultylogo")
    slug = models.SlugField(max_length=255)
    main_page = models.BooleanField(default=False)
    description = RichTextField()
    # sections
    kafedras = RichTextField("Tarkibidagi kafedralar", null=True, blank=True)
    directions = RichTextField("Ta’lim yo‘nalishlari", null=True, blank=True)
    history = RichTextField("Fakultet tarixi", null=True, blank=True)
    study_works = RichTextField("O‘quv-uslubiy ishlar", null=True, blank=True)
    spiritual_directions = RichTextField(
        "Fakultet manaviy-marifiy va axloqiy tarbiya ishlari doirasida amalga oshiriladigan yo'nalishlar",
        null=True,
        blank=True,
    )
    research_works = RichTextField("Ilmiy tadqiqot ishlar", null=True, blank=True)
    innovative_works = RichTextField("Innovatsion ishlar", null=True, blank=True)
    faculty_innovative_works = RichTextField(
        "Fakultetda olib borilayotgan innovatsion ishlar", null=True, blank=True
    )
    cooperation = RichTextField("Akademik litsey va kasb-hunar kollejlari bilan hamkorlik", null=True, blank=True)
    international_relations = RichTextField("Xalqaro aloqalar", null=True, blank=True)
    faculty_international_relations = RichTextField("Fakultetning xalqaro aloqalari", null=True, blank=True)
    link = models.URLField("Link", null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "departments"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        return "%s%s" % (settings.HOST, self.image.url) if self.image else ""

    @property
    def type(self):
        return "department"

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.kafedras_uz:
            self.kafedras_sr = generate_field(self.kafedras_uz)
        if self.directions_uz:
            self.directions_sr = generate_field(self.directions_uz)
        if self.history_uz:
            self.history_sr = generate_field(self.history_uz)
        if self.study_works_uz:
            self.study_works_sr = generate_field(self.study_works_uz)
        if self.spiritual_directions_uz:
            self.spiritual_directions_sr = generate_field(self.spiritual_directions_uz)
        if self.research_works_uz:
            self.research_works_sr = generate_field(self.research_works_uz)
        if self.innovative_works_uz:
            self.innovative_works_sr = generate_field(self.innovative_works_uz)
        if self.faculty_innovative_works_uz:
            self.faculty_innovative_works_sr = generate_field(self.faculty_innovative_works_uz)
        if self.cooperation_uz:
            self.cooperation_sr = generate_field(self.cooperation_uz)
        if self.international_relations_uz:
            self.international_relations_sr = generate_field(self.international_relations_uz)
        if self.faculty_international_relations_uz:
            self.faculty_international_relations_sr = generate_field(self.faculty_international_relations_uz)
        # if self.content_uz:
        #     self.content_sr = generate_field(self.content_uz)
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(Department, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(Department, self.title_sr)
        super(Department, self).save(*args, **kwargs)


class DepartmentInfo(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="info")
    title = models.CharField(max_length=255)
    content = RichTextField(null=True)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "department_info"
        ordering = ["order", "created_at"]

    def __str__(self):
        return str(self.title)


class Kafedra(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    faculty = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name="kafedralar")
    mudir = models.ForeignKey("Staff", on_delete=models.SET_NULL, null=True, related_name="kafedra_mudir")
    about = RichTextField()
    # teachers = models.ManyToManyField(Staff,blank=True,related_name='kafedra')
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "kafedra"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.about_uz:
            self.about_sr = generate_field(self.about_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        if self.slug:  # edit
            if slugify(self.title_sr) != self.slug:
                self.slug = generate_unique_slug(Kafedra, self.title_sr)
        else:  # create
            self.slug = generate_unique_slug(Kafedra, self.title_sr)
        super(Kafedra, self).save(*args, **kwargs)


# General staff model (only BOOL fields will be filtered in view)
class Staff(models.Model):
    title = models.CharField(max_length=355)
    name = models.CharField(_("Name"), max_length=355, null=True, blank=True)
    order = models.IntegerField(null=True)
    position = models.CharField(max_length=500, null=True)
    # degree = models.CharField(max_length=500, null=True)
    reception_days = models.CharField(max_length=255, null=True)
    duty = RichTextField(editable=False, null=True, blank=True)
    work_history = RichTextField(null=True, blank=True, editable=False)
    # new fields
    bio = RichTextField(null=True, blank=True)
    task = RichTextField(null=True, blank=True)
    # ADD NEW FIELD FOR NAME
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    fax = models.CharField(max_length=32, null=True, blank=True)
    image = ResizedImageField(size=STAFF_IMAGE, upload_to="staff")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name="staffs")
    kafedra = models.ForeignKey(Kafedra, on_delete=models.SET_NULL, null=True, blank=True, related_name="staffs")
    organization = models.ForeignKey(
        "Organization", on_delete=models.SET_NULL, null=True, blank=True, related_name="staffs"
    )
    facebook = models.URLField(verbose_name="Facebook", null=True, blank=True)
    instagram = models.URLField(verbose_name="Instagram", null=True, blank=True)
    linkedin = models.URLField(verbose_name="Linkedin", null=True, blank=True)
    main = models.BooleanField(default=False)
    leader = models.BooleanField(default=False)
    rector = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "staff"
        ordering = ["-rector", "order", "-leader", "-main"]

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.position_uz:
            self.position_sr = generate_field(self.position_uz)
        if self.reception_days_uz:
            self.reception_days_sr = generate_field(self.reception_days_uz)
        if self.work_history_uz:
            self.work_history_sr = generate_field(self.work_history_uz)
        if self.duty_uz:
            self.duty_sr = generate_field(self.duty_uz)

        super(Staff, self).save(*args, **kwargs)


class StaffGallery(models.Model):
    image = ResizedImageField(size=IMAGE, upload_to="staff_gallery")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name="gallery")


class RegionalDepartment(models.Model):
    title = models.CharField(max_length=500)
    address = RichTextField(null=True)
    address_url = models.URLField(null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(null=True, blank=True)
    director = models.CharField(max_length=200)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "regional_department"
        ordering = ["created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)
        if self.director_uz:
            self.director_sr = generate_field(self.director_uz)
        super(RegionalDepartment, self).save(*args, **kwargs)


# Extra organization for STAFF
class Organization(models.Model):
    title = models.CharField(max_length=500)
    content = RichTextField(null=True)
    org_type = models.SmallIntegerField(choices=((1, "Markaz"), (2, "Bo'lim"), (3, "Departament")))
    # views = models.IntegerField(default=0)
    # publish_date = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    reg_link = models.URLField(null=True, blank=True)
    reg_image = models.ImageField(null=True, blank=True)
    reg_title = models.CharField(max_length=255, null=True, blank=True)
    reg_subtitle = models.CharField(max_length=255, null=True, blank=True)

    slug = models.SlugField(max_length=200)

    class Meta:
        db_table = "organizations"
        ordering = ["-created_at"]

    @property
    def reg_image_url(self):
        # "Returns the image url."
        if self.reg_image:
            return "%s%s" % (settings.HOST, self.reg_image.url)
        return ""

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        if hasattr(self, "slug") and hasattr(self, "title_sr"):  # edit
            if self.slug:
                pass
            else:  # create
                self.slug = generate_unique_slug(self.__class__, self.title_sr)
        super(Organization, self).save(*args, **kwargs)


# qo'shma dasturlar
class StudyProgram(models.Model):
    title = models.CharField(max_length=200, null=True)
    image = ResizedImageField(size=[893, 497])
    description = RichTextField()
    bachelor = RichTextField()
    bachelor_documents = RichTextField()
    master = RichTextField()
    # master_documents = models.TextField()
    content = RichTextField()

    views = models.IntegerField(default=0)

    publish_date = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_page = models.BooleanField(default=True)
    link = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "study_programs"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    # @property
    # def file_url(self):
    #     # "Returns the image url."
    #     if self.file:
    #         return '%s%s' % (settings.HOST, self.file.url)
    #     return ''

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.description_uz:
            self.description_sr = generate_field(self.description_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)

        super(StudyProgram, self).save(*args, **kwargs)


# sirtqi bo'lim
class NightProgram(models.Model):
    title = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    fax = models.CharField(max_length=32, null=True, blank=True)
    content = RichTextField()
    goals_tasks = RichTextField()
    tasks = RichTextField()
    bachelor = RichTextField()
    directions = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "night_program"
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.title)

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.address_uz:
            self.address_sr = generate_field(self.address_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        if self.goals_tasks_uz:
            self.goals_tasks_sr = generate_field(self.goals_tasks_uz)
        if self.bachelor_uz:
            self.bachelor_sr = generate_field(self.bachelor_uz)
        if self.directions_uz:
            self.directions_sr = generate_field(self.directions_uz)
        super(NightProgram, self).save(*args, **kwargs)


# ilmiy kengash tarkibi
class CouncilStaff(models.Model):
    title = models.CharField(max_length=355)
    image = ResizedImageField(size=[75, 72], upload_to="staff")
    shifr = models.CharField(max_length=20, null=True)
    about = models.CharField(max_length=500, null=True)
    # degree = models.CharField(max_length=500, null=True)
    order = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "council_staff"
        ordering = ["order"]

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.about_uz:
            self.about_sr = generate_field(self.about_uz)
        super(CouncilStaff, self).save(*args, **kwargs)


# kengash
class Council(models.Model):
    title = models.CharField(max_length=355)
    image = ResizedImageField(upload_to="staff", null=True, blank=True)
    content = RichTextField()
    order = models.IntegerField(default=0)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "council"
        ordering = ["order"]

    def __str__(self):
        return str(self.title)

    @property
    def image_url(self):
        # "Returns the image url."
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return ""

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        super(Council, self).save(*args, **kwargs)


# class Camp(models.Model):
#     content = models.TextField()
#     long = models.DecimalField(max_digits=10, decimal_places=6, null=True)
#     lat = models.DecimalField(max_digits=10, decimal_places=6, null=True)
#
#     def __str__(self):
#         return str(self.id)

# class CampImage(models.Model):
#     camp = models.ForeignKey(
#         Camp, on_delete=models.CASCADE, related_name='images')
#     image = ResizedImageField(size=IMAGE, upload_to='camp_photos')
#
#     class Meta:
#         db_table = 'camp_images'
#         ordering = ['id']
#
#     def __str__(self):
#         return self.image.name
#
#     @property
#     def url(self):
#         # "Returns the image url."
#         return '%s%s' % (settings.HOST, self.image.url)


class RectorCongratulation(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(default=timezone.now)
    image = models.FileField(upload_to="rector")
    content = RichTextField()
    rector_fullname = models.CharField(max_length=255)
    instagram = models.URLField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)

    class Meta:
        db_table = "rector_cong"

    def __str__(self):
        return self.rector_fullname

    @property
    def rector_image(self):
        if self.image:
            return "%s%s" % (settings.HOST, self.image.url)
        return None

    @property
    def image_name(self):
        if self.image:
            return os.path.basename(self.image.name)
        return None

    def save(self, *args, **kwargs):
        if self.title_uz:
            self.title_sr = generate_field(self.title_uz)
        if self.content_uz:
            self.content_sr = generate_field(self.content_uz)
        if self.rector_fullname_uz:
            self.rector_fullname_sr = generate_field(self.rector_fullname_uz)
        super(RectorCongratulation, self).save(*args, **kwargs)


class Ustav(models.Model):
    title = models.CharField(max_length=255)
    sub_title = models.CharField(max_length=255, null=True)
    short_description = RichTextField()
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ["order"]


class UnversityFile(models.Model):
    slug = models.SlugField(unique=True)
    file = models.FileField(upload_to="unversitet", null=True)

    @property
    def file_url(self):
        if self.file:
            return "%s%s" % (settings.HOST, self.file.url)
        return None
